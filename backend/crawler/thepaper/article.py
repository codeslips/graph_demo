"""
ThePaper article detail parser.

Fetches and parses individual article pages.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup

from ..utils.http_client import HttpClient
from .config import DETAIL_PAGE_URL, REQUEST_DELAY

logger = logging.getLogger(__name__)


def parse_article_html(html: str, cont_id: str, url: str) -> dict[str, Any]:
    """
    Parse article HTML and extract structured data from __NEXT_DATA__ script.

    Args:
        html: The HTML content of the article page
        cont_id: The content ID of the article
        url: The URL of the article

    Returns:
        Structured article data as dictionary
    """
    soup = BeautifulSoup(html, "lxml")

    # Find the __NEXT_DATA__ script tag which contains all article data
    next_data_script = soup.find("script", id="__NEXT_DATA__")

    if next_data_script and next_data_script.string:
        try:
            next_data = json.loads(next_data_script.string)
            content_detail = (
                next_data.get("props", {})
                .get("pageProps", {})
                .get("detailData", {})
                .get("contentDetail", {})
            )

            if content_detail:
                # Extract node/channel info
                node_info = content_detail.get("nodeInfo", {})

                # Parse content HTML to extract paragraphs
                content_html = content_detail.get("content", "")
                content_paragraphs = []
                if content_html:
                    content_soup = BeautifulSoup(content_html, "lxml")
                    for p in content_soup.find_all("p"):
                        text = p.get_text(strip=True)
                        if text:
                            content_paragraphs.append(text)

                # Extract tags
                tags = []
                tag_list = content_detail.get("tagList", [])
                for tag in tag_list:
                    tags.append(
                        {
                            "tagId": tag.get("tagId"),
                            "tag": tag.get("tag"),
                        }
                    )

                # Parse publish time
                pub_time_str = content_detail.get("pubTime", "")
                publish_time = None
                if pub_time_str:
                    try:
                        publish_time = datetime.strptime(
                            pub_time_str, "%Y-%m-%d %H:%M"
                        )
                    except ValueError:
                        logger.warning(f"Could not parse publish time: {pub_time_str}")

                return {
                    "contId": cont_id,
                    "url": url,
                    "title": content_detail.get("name", ""),
                    "summary": content_detail.get("summary", ""),
                    "author": content_detail.get("author", ""),
                    "pubTime": pub_time_str,
                    "publishTime": publish_time,
                    "channel": {
                        "nodeId": node_info.get("nodeId"),
                        "name": node_info.get("name", ""),
                        "desc": node_info.get("desc", ""),
                    },
                    "content": content_paragraphs,
                    "contentText": "\n\n".join(content_paragraphs),
                    "tags": tags,
                    "pic": content_detail.get("pic", ""),
                }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse __NEXT_DATA__ JSON: {e}")

    # Fallback: return minimal data if parsing failed
    return {
        "contId": cont_id,
        "url": url,
        "title": "",
        "error": "Failed to parse article data",
    }


async def fetch_article_detail(
    cont_id: str,
    client: HttpClient | None = None,
) -> dict[str, Any]:
    """
    Fetch and parse article detail by content ID.

    Args:
        cont_id: The content ID of the article
        client: Optional HttpClient for connection reuse

    Returns:
        Parsed article data as dictionary
    """
    url = DETAIL_PAGE_URL.format(cont_id=cont_id)

    if client is None:
        async with HttpClient() as new_client:
            response = await new_client.get(url)
            html = response.text
            return parse_article_html(html, cont_id, url)
    else:
        response = await client.get(url)
        html = response.text
        return parse_article_html(html, cont_id, url)


async def fetch_multiple_articles(
    cont_ids: list[str],
    delay: float = REQUEST_DELAY,
) -> list[dict[str, Any]]:
    """
    Fetch multiple article details with rate limiting.

    Args:
        cont_ids: List of content IDs to fetch
        delay: Delay between requests in seconds

    Returns:
        List of article detail responses
    """
    results: list[dict[str, Any]] = []

    async with HttpClient() as client:
        for i, cont_id in enumerate(cont_ids):
            try:
                logger.info(f"[{i + 1}/{len(cont_ids)}] Fetching article: {cont_id}")
                detail = await fetch_article_detail(cont_id, client)
                results.append(detail)

                # Delay between requests to avoid rate limiting
                if i < len(cont_ids) - 1:
                    await asyncio.sleep(delay)

            except Exception as e:
                logger.error(f"Error fetching article {cont_id}: {e}")
                results.append(
                    {
                        "contId": cont_id,
                        "error": str(e),
                    }
                )

    return results

