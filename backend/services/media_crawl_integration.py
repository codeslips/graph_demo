# -*- coding: utf-8 -*-
"""
Media crawl integration service.

Provides optional integration between CrawlTask and media platform crawling.
This integration is controlled by MEDIA_CRAWL_INTEGRATION_ENABLED setting.
"""

from enum import Enum
from typing import Optional

from django.conf import settings


class MediaPlatform(str, Enum):
    """Supported media platforms."""

    BILIBILI = "bilibili"
    DOUYIN = "douyin"
    KUAISHOU = "kuaishou"
    WEIBO = "weibo"
    XHS = "xhs"
    TIEBA = "tieba"
    ZHIHU = "zhihu"


def is_integration_enabled() -> bool:
    """Check if media crawl integration is enabled."""
    return getattr(settings, "MEDIA_CRAWL_INTEGRATION_ENABLED", False)


def is_media_crawl_enabled() -> bool:
    """Check if media crawl feature is enabled."""
    return getattr(settings, "MEDIA_CRAWL_ENABLED", True)


def get_platform_from_url(url: str) -> Optional[MediaPlatform]:
    """
    Detect media platform from URL.

    Args:
        url: URL to analyze

    Returns:
        MediaPlatform enum or None if not a supported platform
    """
    url_lower = url.lower()

    platform_patterns = {
        MediaPlatform.BILIBILI: ["bilibili.com", "b23.tv"],
        MediaPlatform.DOUYIN: ["douyin.com", "iesdouyin.com"],
        MediaPlatform.KUAISHOU: ["kuaishou.com", "kwai.com"],
        MediaPlatform.WEIBO: ["weibo.com", "weibo.cn"],
        MediaPlatform.XHS: ["xiaohongshu.com", "xhslink.com"],
        MediaPlatform.TIEBA: ["tieba.baidu.com"],
        MediaPlatform.ZHIHU: ["zhihu.com"],
    }

    for platform, patterns in platform_patterns.items():
        if any(pattern in url_lower for pattern in patterns):
            return platform

    return None


def should_trigger_media_crawl(url: str) -> bool:
    """
    Check if a URL should trigger media platform crawling.

    Args:
        url: Target URL

    Returns:
        True if media crawl should be triggered
    """
    if not is_integration_enabled():
        return False

    if not is_media_crawl_enabled():
        return False

    platform = get_platform_from_url(url)
    return platform is not None


def trigger_media_crawl(url: str, task_id: str) -> Optional[str]:
    """
    Trigger media platform crawl for a given URL.

    This is a placeholder for future implementation.
    The actual crawl logic will be implemented separately.

    Args:
        url: Target URL to crawl
        task_id: Parent CrawlTask ID for reference

    Returns:
        Media crawl task ID if triggered, None otherwise
    """
    if not should_trigger_media_crawl(url):
        return None

    platform = get_platform_from_url(url)
    if not platform:
        return None

    # TODO: Implement actual crawl triggering
    # This will be implemented when crawl logic is added
    # For now, just log and return None

    import logging

    logger = logging.getLogger(__name__)
    logger.info(
        f"Media crawl triggered for {platform.value}: {url} (parent task: {task_id})"
    )

    return None

