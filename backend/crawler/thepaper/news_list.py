"""
ThePaper channel/news list crawler.

Fetches article lists from ThePaper's channel API.
"""

import logging
from typing import Any

from ..utils.http_client import HttpClient
from .config import CHANNEL_API_URL, DEFAULT_CHANNEL_ID, DEFAULT_PAGE_SIZE

logger = logging.getLogger(__name__)


async def fetch_channel_content(
    channel_id: str = DEFAULT_CHANNEL_ID,
    page_num: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
    start_time: int | None = None,
    exclude_cont_ids: list[int] | None = None,
) -> dict[str, Any]:
    """
    Fetch content from ThePaper channel API.

    Args:
        channel_id: The channel ID to fetch content from
        page_num: Page number for pagination
        page_size: Number of items per page
        start_time: Timestamp for pagination cursor
        exclude_cont_ids: List of content IDs to exclude

    Returns:
        API response as dictionary with structure:
        {
            "code": 200,
            "data": {
                "list": [...],
                "hasNext": bool,
                "startTime": int,
                ...
            }
        }
    """
    payload: dict[str, Any] = {
        "channelId": channel_id,
        "excludeContIds": exclude_cont_ids or [],
        "listRecommendIds": [],
        "province": None,
        "pageSize": page_size,
        "pageNum": page_num,
    }

    if start_time is not None:
        payload["startTime"] = start_time

    async with HttpClient() as client:
        logger.info(f"Fetching channel {channel_id} page {page_num}")
        response = await client.post(CHANNEL_API_URL, json=payload)
        data = response.json()

        if data.get("code") != 200:
            logger.error(f"API error: {data.get('msg', 'Unknown error')}")
            raise ValueError(f"API returned error: {data.get('msg')}")

        return data


async def fetch_all_channel_content(
    channel_id: str = DEFAULT_CHANNEL_ID,
    max_pages: int = 3,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> list[dict[str, Any]]:
    """
    Fetch multiple pages of content from a channel.

    Args:
        channel_id: The channel ID to fetch content from
        max_pages: Maximum number of pages to fetch
        page_size: Number of items per page

    Returns:
        List of all articles from all pages
    """
    all_items: list[dict[str, Any]] = []
    start_time: int | None = None
    exclude_ids: list[int] = []

    for page_num in range(1, max_pages + 1):
        try:
            result = await fetch_channel_content(
                channel_id=channel_id,
                page_num=page_num,
                page_size=page_size,
                start_time=start_time,
                exclude_cont_ids=exclude_ids,
            )

            data = result.get("data", {})
            items = data.get("list", [])

            if not items:
                logger.info(f"No more items at page {page_num}")
                break

            all_items.extend(items)

            # Update pagination cursor
            start_time = data.get("startTime")
            exclude_ids = [item.get("contId") for item in items if item.get("contId")]

            # Check if there are more pages
            if not data.get("hasNext", False):
                logger.info(f"Reached last page at {page_num}")
                break

            logger.info(f"Fetched page {page_num}, total items: {len(all_items)}")

        except Exception as e:
            logger.error(f"Error fetching page {page_num}: {e}")
            break

    return all_items


def extract_channel_id_from_url(url: str) -> str:
    """
    Extract channel ID from ThePaper URL.

    Args:
        url: ThePaper channel URL

    Returns:
        Channel ID string
    """
    # Handle various URL formats:
    # https://www.thepaper.cn/channel_25953
    # https://www.thepaper.cn/list_25953
    import re

    patterns = [
        r"channel[_/](\d+)",
        r"list[_/](\d+)",
        r"nodeId=(\d+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # Return default if no match
    return DEFAULT_CHANNEL_ID

