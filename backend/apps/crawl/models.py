"""
Crawl models.

CrawlTask and CrawlItem models for tracking crawl jobs and results.
"""

import uuid

from django.db import models
from django.utils import timezone

from .enums import CrawlType, TaskStatus


class CrawlTask(models.Model):
    """
    Represents a crawl job with status tracking.

    Tracks the lifecycle of a crawl operation from creation through
    execution to completion or failure.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_url = models.CharField(max_length=500, help_text="Target URL to crawl")
    crawl_type = models.CharField(
        max_length=50,
        choices=CrawlType.choices,
        default=CrawlType.NEWS_LIST,
        help_text="Type of crawl operation",
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING,
        db_index=True,
        help_text="Current task status",
    )
    total_items = models.PositiveIntegerField(
        default=0, help_text="Number of items crawled"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, help_text="Error details if failed")
    celery_task_id = models.CharField(
        max_length=255, blank=True, help_text="Celery task ID for tracking"
    )

    class Meta:
        db_table = "crawl_task"
        ordering = ["-created_at"]
        verbose_name = "Crawl Task"
        verbose_name_plural = "Crawl Tasks"

    def __str__(self) -> str:
        return f"CrawlTask({self.id}) - {self.status}"

    def mark_running(self) -> None:
        """Mark task as running."""
        self.status = TaskStatus.RUNNING
        self.started_at = timezone.now()
        self.save(update_fields=["status", "started_at"])

    def mark_done(self, total_items: int = 0) -> None:
        """Mark task as done."""
        self.status = TaskStatus.DONE
        self.total_items = total_items
        self.finished_at = timezone.now()
        self.save(update_fields=["status", "total_items", "finished_at"])

    def mark_failed(self, error_message: str) -> None:
        """Mark task as failed with error message."""
        self.status = TaskStatus.FAILED
        self.error_message = error_message
        self.finished_at = timezone.now()
        self.save(update_fields=["status", "error_message", "finished_at"])


class CrawlItem(models.Model):
    """
    Represents an individual crawled article.

    Stores metadata about each article crawled as part of a CrawlTask.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(
        CrawlTask,
        on_delete=models.CASCADE,
        related_name="items",
        help_text="Parent crawl task",
    )

    # Article identifiers
    cont_id = models.CharField(
        max_length=50, unique=True, help_text="ThePaper content ID"
    )
    url = models.CharField(max_length=500, help_text="Article URL")

    # Article content
    title = models.CharField(max_length=500, help_text="Article title")
    author = models.CharField(max_length=200, blank=True, help_text="Article author")
    summary = models.TextField(blank=True, help_text="Article summary")
    content_text = models.TextField(blank=True, help_text="Full article text")

    # Channel/category info
    channel_id = models.IntegerField(null=True, blank=True, help_text="Channel node ID")
    channel_name = models.CharField(
        max_length=100, blank=True, help_text="Channel name"
    )

    # Timestamps
    publish_time = models.DateTimeField(
        null=True, blank=True, help_text="Article publish time"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Tags stored as JSON
    tags = models.JSONField(default=list, help_text="List of tag objects")

    # Sync status
    neo4j_synced = models.BooleanField(
        default=False, db_index=True, help_text="Whether synced to Neo4j"
    )

    class Meta:
        db_table = "crawl_item"
        ordering = ["-created_at"]
        verbose_name = "Crawl Item"
        verbose_name_plural = "Crawl Items"
        indexes = [
            models.Index(fields=["task", "neo4j_synced"]),
        ]

    def __str__(self) -> str:
        return f"CrawlItem({self.cont_id}) - {self.title[:50]}"
