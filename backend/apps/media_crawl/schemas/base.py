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

