"""
ThePaper crawler configuration.

API URLs, headers, and default settings for crawling ThePaper.cn
"""

from django.conf import settings

# API endpoints
CHANNEL_API_URL = "https://api.thepaper.cn/contentapi/nodeCont/getByChannelId"
DETAIL_PAGE_URL = "https://m.thepaper.cn/newsDetail_forward_{cont_id}"

# Default channel ID (生活 - Life channel)
DEFAULT_CHANNEL_ID = "25953"

# Request headers
DEFAULT_HEADERS = {
    "User-Agent": getattr(
        settings,
        "CRAWL_USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Origin": "https://www.thepaper.cn",
    "Referer": "https://www.thepaper.cn/",
}

# Crawler settings with fallbacks
REQUEST_DELAY = getattr(settings, "CRAWL_REQUEST_DELAY", 0.5)
MAX_RETRIES = getattr(settings, "CRAWL_MAX_RETRIES", 3)
REQUEST_TIMEOUT = getattr(settings, "CRAWL_TIMEOUT", 30)

# Pagination defaults
DEFAULT_PAGE_SIZE = 20
DEFAULT_MAX_PAGES = 3

