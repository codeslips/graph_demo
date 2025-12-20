"""
Crawl task status enums.
"""

from django.db import models


class TaskStatus(models.TextChoices):
    """Status choices for CrawlTask."""

    PENDING = "PENDING", "Pending"
    RUNNING = "RUNNING", "Running"
    DONE = "DONE", "Done"
    FAILED = "FAILED", "Failed"


class CrawlType(models.TextChoices):
    """Types of crawl operations."""

    NEWS_LIST = "news_list", "News List"
    ARTICLE = "article", "Single Article"
    CHANNEL = "channel", "Full Channel"


class MediaPlatform(models.TextChoices):
    """Supported media platforms for optional media crawl integration."""

    NONE = "", "None"
    BILIBILI = "bilibili", "Bilibili"
    DOUYIN = "douyin", "Douyin"
    KUAISHOU = "kuaishou", "Kuaishou"
    WEIBO = "weibo", "Weibo"
    XHS = "xhs", "Xiaohongshu"
    TIEBA = "tieba", "Tieba"
    ZHIHU = "zhihu", "Zhihu"

