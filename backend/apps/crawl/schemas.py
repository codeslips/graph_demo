"""
Django Ninja schemas for crawl API.

Request and response schemas for crawl task endpoints.
"""

from datetime import datetime
from typing import Any
from uuid import UUID

from ninja import Schema

from .enums import CrawlType, TaskStatus


class CreateTaskRequest(Schema):
    """Request schema for creating a crawl task."""

    target_url: str
    crawl_type: str = CrawlType.NEWS_LIST.value
    media_platform: str = ""
    media_crawl_enabled: bool = False


class TaskResponse(Schema):
    """Response schema for a single crawl task."""

    id: UUID
    target_url: str
    crawl_type: str
    status: str
    total_items: int
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_message: str = ""
    media_platform: str = ""
    media_crawl_enabled: bool = False

    @staticmethod
    def from_orm(obj) -> "TaskResponse":
        """Convert ORM object to schema."""
        return TaskResponse(
            id=obj.id,
            target_url=obj.target_url,
            crawl_type=obj.crawl_type,
            status=obj.status,
            total_items=obj.total_items,
            created_at=obj.created_at,
            started_at=obj.started_at,
            finished_at=obj.finished_at,
            error_message=obj.error_message,
            media_platform=obj.media_platform,
            media_crawl_enabled=obj.media_crawl_enabled,
        )


class TaskListResponse(Schema):
    """Response schema for list of tasks."""

    items: list[TaskResponse]
    total: int
    page: int
    page_size: int
    has_next: bool


class TaskDetailResponse(TaskResponse):
    """Extended response with item count."""

    celery_task_id: str = ""


class CrawlItemResponse(Schema):
    """Response schema for a crawl item."""

    id: UUID
    cont_id: str
    url: str
    title: str
    author: str
    summary: str
    channel_name: str
    publish_time: datetime | None = None
    tags: list[dict[str, Any]]
    neo4j_synced: bool
    created_at: datetime

    @staticmethod
    def from_orm(obj) -> "CrawlItemResponse":
        """Convert ORM object to schema."""
        return CrawlItemResponse(
            id=obj.id,
            cont_id=obj.cont_id,
            url=obj.url,
            title=obj.title,
            author=obj.author,
            summary=obj.summary,
            channel_name=obj.channel_name,
            publish_time=obj.publish_time,
            tags=obj.tags,
            neo4j_synced=obj.neo4j_synced,
            created_at=obj.created_at,
        )


class ItemListResponse(Schema):
    """Response schema for list of items."""

    items: list[CrawlItemResponse]
    total: int
    page: int
    page_size: int


class ErrorResponse(Schema):
    """Error response schema."""

    error: str
    detail: str = ""

