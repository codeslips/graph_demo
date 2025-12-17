#!/usr/bin/env python3
"""
Basic crawler script for ThePaper (澎湃新闻) API.

Uses aiohttp to fetch news content from ThePaper's API endpoint.
Uses BeautifulSoup to parse article detail HTML pages.
"""

import asyncio
import json
from pathlib import Path
from typing import Any

import aiohttp
from bs4 import BeautifulSoup


# API URLs
CHANNEL_API_URL = "https://api.thepaper.cn/contentapi/nodeCont/getByChannelId"
DETAIL_PAGE_URL = "https://m.thepaper.cn/newsDetail_forward_{cont_id}"

# Default headers to mimic browser request
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Origin": "https://www.thepaper.cn",
    "Referer": "https://www.thepaper.cn/",
}

# Details output directory
DETAILS_DIR = Path(__file__).parent / "details"


async def fetch_channel_content(
    channel_id: str = "25953",
    page_num: int = 1,
    page_size: int = 20,
    start_time: int | None = None,
    exclude_cont_ids: list[int] | None = None,
    list_recommend_ids: list[int] | None = None,
    province: str | None = None,
) -> dict[str, Any]:
    """
    Fetch content from ThePaper channel API.

    Args:
        channel_id: The channel ID to fetch content from
        page_num: Page number for pagination
        page_size: Number of items per page
        start_time: Timestamp for pagination cursor
        exclude_cont_ids: List of content IDs to exclude
        list_recommend_ids: List of recommended content IDs
        province: Province filter (optional)

    Returns:
        API response as dictionary
    """
    payload = {
        "channelId": channel_id,
        "excludeContIds": exclude_cont_ids or [],
        "listRecommendIds": list_recommend_ids or [],
        "province": province,
        "pageSize": page_size,
        "pageNum": page_num,
    }

    # Add startTime if provided
    if start_time is not None:
        payload["startTime"] = start_time

    async with aiohttp.ClientSession(headers=DEFAULT_HEADERS) as session:
        async with session.post(CHANNEL_API_URL, json=payload) as response:
            response.raise_for_status()
            data = await response.json()
            return data


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

                # Extract images from content or images array
                images = []
                images_data = content_detail.get("images", [])
                for img in images_data:
                    img_url = img.get("url") or img.get("src")
                    if img_url:
                        images.append({
                            "url": img_url,
                            "width": img.get("width"),
                            "height": img.get("height"),
                            "description": img.get("description", ""),
                        })

                # Extract tags
                tags = []
                tag_list = content_detail.get("tagList", [])
                for tag in tag_list:
                    tags.append({
                        "tagId": tag.get("tagId"),
                        "tag": tag.get("tag"),
                    })

                return {
                    "contId": cont_id,
                    "url": url,
                    "title": content_detail.get("name", ""),
                    "summary": content_detail.get("summary", ""),
                    "author": content_detail.get("author", ""),
                    "pubTime": content_detail.get("pubTime", ""),
                    "publishTimestamp": content_detail.get("publishTime"),
                    "channel": {
                        "nodeId": node_info.get("nodeId"),
                        "name": node_info.get("name", ""),
                        "desc": node_info.get("desc", ""),
                    },
                    "responEditor": content_detail.get("responEditor", ""),
                    "imageEditor": content_detail.get("imageEditor", ""),
                    "content": content_paragraphs,
                    "contentText": "\n\n".join(content_paragraphs),
                    "contentHtml": content_html,
                    "images": images,
                    "tags": tags,
                    "sharePic": content_detail.get("sharePic", ""),
                    "pic": content_detail.get("pic", ""),
                    "voiceInfo": content_detail.get("voiceInfo"),
                }

        except json.JSONDecodeError as e:
            print(f"  ✗ Failed to parse __NEXT_DATA__ JSON: {e}")

    # Fallback: return minimal data if parsing failed
    return {
        "contId": cont_id,
        "url": url,
        "title": "",
        "error": "Failed to parse article data",
    }


async def fetch_article_detail(
    cont_id: str,
    session: aiohttp.ClientSession | None = None,
) -> dict[str, Any]:
    """
    Fetch and parse article detail by content ID.

    Args:
        cont_id: The content ID of the article
        session: Optional aiohttp session for connection reuse

    Returns:
        Parsed article data as dictionary
    """
    url = DETAIL_PAGE_URL.format(cont_id=cont_id)

    if session is None:
        async with aiohttp.ClientSession(headers=DEFAULT_HEADERS) as new_session:
            async with new_session.get(url) as response:
                response.raise_for_status()
                html = await response.text()
                return parse_article_html(html, cont_id, url)
    else:
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()
            return parse_article_html(html, cont_id, url)


async def crawl_article_details(
    cont_ids: list[str],
    delay: float = 0.5,
) -> list[dict[str, Any]]:
    """
    Crawl multiple article details and save to files.

    Args:
        cont_ids: List of content IDs to fetch
        delay: Delay between requests in seconds

    Returns:
        List of article detail responses
    """
    # Ensure details directory exists
    DETAILS_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    async with aiohttp.ClientSession(headers=DEFAULT_HEADERS) as session:
        for i, cont_id in enumerate(cont_ids):
            try:
                print(f"[{i+1}/{len(cont_ids)}] Fetching article: {cont_id}")
                detail = await fetch_article_detail(cont_id, session)

                # Save to file
                output_file = DETAILS_DIR / f"{cont_id}.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(detail, f, ensure_ascii=False, indent=2)

                print(f"  ✓ Saved to {output_file.name}")
                results.append(detail)

                # Delay between requests to avoid rate limiting
                if i < len(cont_ids) - 1:
                    await asyncio.sleep(delay)

            except aiohttp.ClientResponseError as e:
                print(f"  ✗ HTTP Error: {e.status} - {e.message}")
            except Exception as e:
                print(f"  ✗ Error: {e}")

    return results


async def crawl_details_from_list(
    list_file: str | Path = "list.json",
    delay: float = 0.5,
) -> list[dict[str, Any]]:
    """
    Read list.json and crawl all article details.

    Args:
        list_file: Path to the list.json file
        delay: Delay between requests in seconds

    Returns:
        List of article detail responses
    """
    list_path = Path(list_file)
    if not list_path.is_absolute():
        list_path = Path(__file__).parent / list_file

    if not list_path.exists():
        print(f"Error: {list_path} not found")
        return []

    with open(list_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract contIds from list
    items = data.get("data", {}).get("list", [])
    cont_ids = [item.get("contId") for item in items if item.get("contId")]

    print(f"Found {len(cont_ids)} articles to crawl")
    print(f"Details will be saved to: {DETAILS_DIR}")
    print("-" * 50)

    return await crawl_article_details(cont_ids, delay)


async def main() -> None:
    """Main entry point for the crawler."""
    # Example: Fetch content with the provided payload
    try:
        result = await fetch_channel_content(
            channel_id="25953",
            page_num=4,
            page_size=20,
            start_time=1765804356345,
            exclude_cont_ids=[32191642, 32102698],
            list_recommend_ids=[32191642],
        )

        print("Response received successfully!")
        print(f"Status code: {result.get('code', 'N/A')}")
        print(f"Message: {result.get('msg', 'N/A')}")

        # Pretty print the full response
        print("\nFull response:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # Extract and display content items if available
        data = result.get("data", {})
        if isinstance(data, dict):
            items = data.get("list", [])
            print(f"\n{'='*50}")
            print(f"Total items in response: {len(items)}")

            for i, item in enumerate(items[:5], 1):  # Show first 5 items
                print(f"\n--- Item {i} ---")
                print(f"Title: {item.get('name', 'N/A')}")
                print(f"Content ID: {item.get('contId', 'N/A')}")
                print(f"Publish Time: {item.get('pubTime', 'N/A')}")
                print(f"Author: {item.get('author', 'N/A')}")

        # Save result to list.json
        with open("list.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nResult saved to list.json")

    except aiohttp.ClientResponseError as e:
        print(f"HTTP Error: {e.status} - {e.message}")
    except aiohttp.ClientError as e:
        print(f"Request Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


async def main_crawl_details() -> None:
    """Main entry point for crawling article details."""
    print("=" * 50)
    print("ThePaper Article Detail Crawler")
    print("=" * 50)

    results = await crawl_details_from_list()

    print("-" * 50)
    print(f"Completed! Crawled {len(results)} articles.")
    print(f"Details saved to: {DETAILS_DIR}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "details":
        # Run: python crawl_thepaper.py details
        asyncio.run(main_crawl_details())
    else:
        # Run: python crawl_thepaper.py
        asyncio.run(main())
