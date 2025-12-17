"""
ThePaper (澎湃新闻) crawler module.

Provides async crawling capabilities for ThePaper news website.
"""

from .article import fetch_article_detail, fetch_multiple_articles, parse_article_html
from .config import CHANNEL_API_URL, DEFAULT_CHANNEL_ID, DETAIL_PAGE_URL
from .news_list import (
    extract_channel_id_from_url,
    fetch_all_channel_content,
    fetch_channel_content,
)

__all__ = [
    # Config
    "CHANNEL_API_URL",
    "DETAIL_PAGE_URL",
    "DEFAULT_CHANNEL_ID",
    # News list
    "fetch_channel_content",
    "fetch_all_channel_content",
    "extract_channel_id_from_url",
    # Article
    "fetch_article_detail",
    "fetch_multiple_articles",
    "parse_article_html",
]
