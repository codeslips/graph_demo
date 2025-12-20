# -*- coding: utf-8 -*-
"""Media Crawl app configuration."""

from django.apps import AppConfig


class MediaCrawlConfig(AppConfig):
    """Configuration for the media_crawl app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.media_crawl"
    verbose_name = "Media Crawl"

