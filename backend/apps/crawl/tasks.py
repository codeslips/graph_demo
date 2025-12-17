"""
Celery tasks for crawl operations.

Provides async task execution for crawling ThePaper news.
"""

import asyncio
import logging
from typing import Any

from asgiref.sync import sync_to_async
from celery import shared_task
from django.utils import timezone

from apps.crawl.enums import TaskStatus
from apps.crawl.models import CrawlItem, CrawlTask
from crawler.thepaper import (
    extract_channel_id_from_url,
    fetch_all_channel_content,
    fetch_article_detail,
)
from crawler.thepaper.config import REQUEST_DELAY
from crawler.utils.http_client import HttpClient

logger = logging.getLogger(__name__)


# Wrap ORM operations for async context
@sync_to_async
def create_crawl_item(**kwargs) -> CrawlItem:
    """Create a CrawlItem in sync context."""
    return CrawlItem.objects.create(**kwargs)


@sync_to_async
def cont_id_exists(cont_id: str) -> bool:
    """Check if a CrawlItem with the given cont_id already exists."""
    return CrawlItem.objects.filter(cont_id=cont_id).exists()


@sync_to_async
def mark_task_done(task: CrawlTask, total_items: int) -> None:
    """Mark task as done in sync context."""
    task.mark_done(total_items=total_items)


@sync_to_async
def sync_neo4j(task_id: str) -> None:
    """Sync to Neo4j in sync context."""
    from services.neo4j_sync import sync_task_to_neo4j
    sync_task_to_neo4j(task_id)


def run_async(coro):
    """Run async coroutine in sync context."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def execute_crawl_task(self, task_id: str) -> dict[str, Any]:
    """
    Execute a crawl task asynchronously.

    This is the main Celery task that orchestrates the crawl operation:
    1. Marks task as RUNNING
    2. Fetches channel content list
    3. Parses each article's detail page
    4. Creates CrawlItem records
    5. Syncs data to Neo4j
    6. Marks task as DONE or FAILED

    Args:
        task_id: UUID of the CrawlTask to execute

    Returns:
        Dictionary with result summary
    """
    logger.info(f"Starting crawl task: {task_id}")

    try:
        # Get the task from database
        task = CrawlTask.objects.get(id=task_id)
    except CrawlTask.DoesNotExist:
        logger.error(f"Task not found: {task_id}")
        return {"error": "Task not found", "task_id": task_id}

    # Update task status to RUNNING
    task.mark_running()
    task.celery_task_id = self.request.id or ""
    task.save(update_fields=["celery_task_id"])

    try:
        # Run the async crawl operation
        result = run_async(_execute_crawl(task))
        return result

    except Exception as e:
        logger.exception(f"Crawl task failed: {task_id}")
        task.mark_failed(str(e))

        # Retry on transient errors
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e)

        return {"error": str(e), "task_id": task_id}


async def _execute_crawl(task: CrawlTask) -> dict[str, Any]:
    """
    Internal async function to execute the crawl.

    Args:
        task: CrawlTask instance to execute

    Returns:
        Dictionary with crawl results
    """
    logger.info(f"Executing crawl for task {task.id}")

    # Extract channel ID from target URL
    channel_id = extract_channel_id_from_url(task.target_url)
    logger.info(f"Channel ID: {channel_id}")

    # Determine max pages based on crawl type
    max_pages = 3 if task.crawl_type == "news_list" else 1

    # Step 1: Fetch article list from channel
    logger.info(f"Fetching channel content (max {max_pages} pages)")
    articles = await fetch_all_channel_content(
        channel_id=channel_id,
        max_pages=max_pages,
        page_size=20,
    )

    if not articles:
        await mark_task_done(task, total_items=0)
        return {"task_id": str(task.id), "items_crawled": 0, "message": "No articles found"}

    logger.info(f"Found {len(articles)} articles to crawl")

    # Step 2: Fetch detail for each article and save
    items_created = 0
    items_skipped = 0
    async with HttpClient() as client:
        for i, article in enumerate(articles):
            cont_id = str(article.get("contId", ""))
            if not cont_id:
                continue

            try:
                # Skip if article already exists in database
                if await cont_id_exists(cont_id):
                    logger.debug(f"[{i + 1}/{len(articles)}] Skipping duplicate: {cont_id}")
                    items_skipped += 1
                    continue

                logger.debug(f"[{i + 1}/{len(articles)}] Fetching article {cont_id}")

                # Fetch article detail
                detail = await fetch_article_detail(cont_id, client)

                # Skip if there was an error
                if detail.get("error"):
                    logger.warning(f"Skipping article {cont_id}: {detail.get('error')}")
                    continue

                # Create CrawlItem record
                channel_info = detail.get("channel", {})
                item = await create_crawl_item(
                    task=task,
                    cont_id=cont_id,
                    url=detail.get("url", ""),
                    title=detail.get("title", ""),
                    author=detail.get("author", ""),
                    summary=detail.get("summary", ""),
                    content_text=detail.get("contentText", ""),
                    channel_id=channel_info.get("nodeId"),
                    channel_name=channel_info.get("name", ""),
                    publish_time=detail.get("publishTime"),
                    tags=detail.get("tags", []),
                    neo4j_synced=False,
                )

                items_created += 1
                logger.debug(f"Created item: {item.cont_id}")

                # Rate limiting
                if i < len(articles) - 1:
                    await asyncio.sleep(REQUEST_DELAY)

            except Exception as e:
                logger.error(f"Error processing article {cont_id}: {e}")
                continue

    # Step 3: Sync to Neo4j
    try:
        logger.info(f"Syncing {items_created} items to Neo4j")
        await sync_neo4j(str(task.id))
    except ImportError:
        logger.warning("Neo4j sync not available yet")
    except Exception as e:
        logger.error(f"Neo4j sync failed: {e}")
        # Continue - items are saved in PostgreSQL

    # Step 4: Mark task as done
    await mark_task_done(task, total_items=items_created)

    if items_skipped > 0:
        logger.info(
            f"Crawl task completed: {task.id}, "
            f"items created: {items_created}, duplicates skipped: {items_skipped}"
        )
    else:
        logger.info(f"Crawl task completed: {task.id}, items: {items_created}")

    return {
        "task_id": str(task.id),
        "items_crawled": items_created,
        "items_skipped": items_skipped,
        "channel_id": channel_id,
        "status": "completed",
    }

