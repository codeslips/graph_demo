# -*- coding: utf-8 -*-
"""Base schemas for media crawl API."""

from typing import Generic, List, Optional, TypeVar

from ninja import Schema


T = TypeVar("T")


class PaginatedResponse(Schema, Generic[T]):
    """Paginated response schema."""

    items: List[T]
    total: int
    limit: int
    offset: int


class ErrorResponse(Schema):
    """Error response schema."""

    detail: str
    code: Optional[str] = None


class SuccessResponse(Schema):
    """Success response schema."""

    success: bool = True
    message: str = "Operation completed successfully"


class BatchDeleteRequest(Schema):
    """Batch delete request schema."""

    ids: List[int]


class BatchDeleteResponse(Schema):
    """Batch delete response schema."""

    deleted_count: int


class TimestampMixin(Schema):
    """Mixin for timestamp fields."""

    add_ts: Optional[int] = None
    last_modify_ts: Optional[int] = None


class FilterParams(Schema):
    """Common filter parameters."""

    user_id: Optional[str] = None
    create_time_from: Optional[int] = None
    create_time_to: Optional[int] = None
    source_keyword: Optional[str] = None


# ============================================================================
# Crawler Task Schemas
# ============================================================================


class CrawlerStartRequest(Schema):
    """Request schema for starting a crawler task."""

    platform: str  # xhs, douyin, bilibili, kuaishou, weibo, tieba, zhihu
    login_type: str  # qrcode, cookie
    crawler_type: str  # search, detail, creator
    keywords: Optional[str] = ""
    specified_ids: Optional[str] = ""
    creator_ids: Optional[str] = ""
    start_page: Optional[int] = 1
    enable_comments: Optional[bool] = True
    enable_sub_comments: Optional[bool] = False
    save_option: Optional[str] = "db"
    cookies: Optional[str] = ""
    headless: Optional[bool] = False


class CrawlerStartResponse(Schema):
    """Response schema for crawler start."""

    success: bool
    message: str


class CrawlerStatusResponse(Schema):
    """Response schema for crawler status."""

    status: str  # running, idle
    platform: Optional[str] = None
    crawler_type: Optional[str] = None
    started_at: Optional[str] = None
    error_message: Optional[str] = None


class CrawlerErrorResponse(Schema):
    """Error response schema for crawler endpoints."""

    detail: str
    code: str

