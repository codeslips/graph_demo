"""
Celery tasks for media crawl operations.

Provides async task execution for syncing media data to Neo4j.
"""

import logging
from typing import Any

from celery import shared_task

from services.media_neo4j_sync import (
    SUPPORTED_PLATFORMS,
    get_sync_status,
    sync_platform_content,
    update_sync_status,
)

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def sync_media_to_neo4j(
    self,
    platform: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """
    Sync media data from MySQL to Neo4j.

    This Celery task syncs media content (videos, notes, posts) and comments
    to Neo4j as graph nodes and relationships.

    Args:
        platform: Platform to sync (bilibili, douyin, kuaishou, weibo, tieba, zhihu)
                  If None, syncs all platforms.
        limit: Maximum content items per platform

    Returns:
        Dictionary with sync results
    """
    task_id = self.request.id or "unknown"
    logger.info(f"Starting media Neo4j sync task: {task_id}")

    # Validate platform
    if platform and platform not in SUPPORTED_PLATFORMS:
        error_msg = f"Unsupported platform: {platform}. Supported: {SUPPORTED_PLATFORMS}"
        logger.error(error_msg)
        return {"error": error_msg, "task_id": task_id}

    # Update status to running
    update_sync_status("running", progress=0)

    try:
        # Calculate total platforms for progress
        platforms_to_sync = [platform] if platform else SUPPORTED_PLATFORMS
        total_platforms = len(platforms_to_sync)

        results: dict[str, Any] = {
            "task_id": task_id,
            "platforms": {},
            "totals": {
                "content_synced": 0,
                "keywords_synced": 0,
                "comments_synced": 0,
            },
        }

        for i, p in enumerate(platforms_to_sync):
            logger.info(f"Syncing platform {i + 1}/{total_platforms}: {p}")

            # Update progress
            progress = int((i / total_platforms) * 100)
            update_sync_status("running", progress=progress)

            # Sync this platform
            platform_result = sync_platform_content(platform=p, limit=limit)

            # Aggregate results
            if "platforms" in platform_result:
                results["platforms"].update(platform_result["platforms"])
                for key in ["content_synced", "keywords_synced", "comments_synced"]:
                    results["totals"][key] += platform_result["totals"].get(key, 0)
            else:
                # Single platform result
                results["platforms"][p] = platform_result.get("platforms", {}).get(p, {})

        # Update status to idle with results
        update_sync_status("idle", progress=100, last_result=results)

        logger.info(f"Media Neo4j sync completed: {results['totals']}")
        return results

    except Exception as e:
        logger.exception(f"Media Neo4j sync failed: {e}")
        update_sync_status("idle", progress=0, last_result={"error": str(e)})

        # Retry on transient errors
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e)

        return {"error": str(e), "task_id": task_id}


@shared_task
def get_media_sync_status() -> dict[str, Any]:
    """
    Get current media Neo4j sync status.

    Returns:
        Current sync status dictionary
    """
    return get_sync_status()

