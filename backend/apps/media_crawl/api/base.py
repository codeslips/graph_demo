# -*- coding: utf-8 -*-
"""Base CRUD API utilities for media crawl."""

from typing import Any, Callable, List, Optional, Type, TypeVar

from django.conf import settings
from django.db.models import Model, Q
from django.http import HttpRequest
from ninja import Router, Schema

from ..schemas.base import (
    BatchDeleteRequest,
    BatchDeleteResponse,
    ErrorResponse,
    PaginatedResponse,
)

ModelType = TypeVar("ModelType", bound=Model)


def check_media_crawl_enabled(request: HttpRequest) -> Optional[ErrorResponse]:
    """Check if media crawl feature is enabled."""
    if not getattr(settings, "MEDIA_CRAWL_ENABLED", True):
        return ErrorResponse(
            detail="Media crawl feature is disabled",
            code="MEDIA_CRAWL_DISABLED",
        )
    return None


def create_crud_router(
    model: Type[ModelType],
    create_schema: Type[Schema],
    update_schema: Type[Schema],
    out_schema: Type[Schema],
    tags: List[str],
    prefix: str = "",
    id_field: str = "id",
    filter_fields: Optional[List[str]] = None,
    time_field: str = "create_time",
) -> Router:
    """
    Create a CRUD router for a model.

    Args:
        model: Django model class
        create_schema: Schema for create requests
        update_schema: Schema for update requests
        out_schema: Schema for response
        tags: API tags
        prefix: URL prefix
        id_field: Primary key field name
        filter_fields: List of fields to filter on
        time_field: Field name for time-based filtering

    Returns:
        Router with CRUD endpoints
    """
    router = Router(tags=tags)
    filter_fields = filter_fields or []

    @router.get(
        "/",
        response={200: PaginatedResponse[out_schema], 503: ErrorResponse},
        summary=f"List {model.__name__}",
    )
    def list_items(
        request: HttpRequest,
        limit: int = 20,
        offset: int = 0,
        user_id: Optional[str] = None,
        create_time_from: Optional[int] = None,
        create_time_to: Optional[int] = None,
        source_keyword: Optional[str] = None,
    ):
        """List items with pagination and filtering."""
        error = check_media_crawl_enabled(request)
        if error:
            return 503, error

        queryset = model.objects.using("mysql").all()

        # Apply filters
        if user_id and "user_id" in [f.name for f in model._meta.get_fields()]:
            queryset = queryset.filter(user_id=user_id)

        if time_field and hasattr(model, time_field):
            if create_time_from:
                queryset = queryset.filter(**{f"{time_field}__gte": create_time_from})
            if create_time_to:
                queryset = queryset.filter(**{f"{time_field}__lte": create_time_to})

        if source_keyword and "source_keyword" in [
            f.name for f in model._meta.get_fields()
        ]:
            queryset = queryset.filter(source_keyword__icontains=source_keyword)

        total = queryset.count()
        items = list(queryset[offset : offset + limit])

        return 200, {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    @router.post(
        "/",
        response={201: out_schema, 422: ErrorResponse, 503: ErrorResponse},
        summary=f"Create {model.__name__}",
    )
    def create_item(request: HttpRequest, payload: create_schema):
        """Create a new item."""
        error = check_media_crawl_enabled(request)
        if error:
            return 503, error

        try:
            item = model.objects.using("mysql").create(**payload.dict())
            return 201, item
        except Exception as e:
            return 422, ErrorResponse(detail=str(e), code="CREATE_ERROR")

    @router.get(
        "/{item_id}/",
        response={200: out_schema, 404: ErrorResponse, 503: ErrorResponse},
        summary=f"Get {model.__name__} by ID",
    )
    def get_item(request: HttpRequest, item_id: int):
        """Get a single item by ID."""
        error = check_media_crawl_enabled(request)
        if error:
            return 503, error

        try:
            item = model.objects.using("mysql").get(pk=item_id)
            return 200, item
        except model.DoesNotExist:
            return 404, ErrorResponse(
                detail=f"{model.__name__} not found", code="NOT_FOUND"
            )

    @router.put(
        "/{item_id}/",
        response={200: out_schema, 404: ErrorResponse, 422: ErrorResponse, 503: ErrorResponse},
        summary=f"Update {model.__name__}",
    )
    def update_item(request: HttpRequest, item_id: int, payload: update_schema):
        """Update an existing item."""
        error = check_media_crawl_enabled(request)
        if error:
            return 503, error

        try:
            item = model.objects.using("mysql").get(pk=item_id)
        except model.DoesNotExist:
            return 404, ErrorResponse(
                detail=f"{model.__name__} not found", code="NOT_FOUND"
            )

        try:
            update_data = payload.dict(exclude_unset=True)
            for field, value in update_data.items():
                if value is not None:
                    setattr(item, field, value)
            item.save(using="mysql")
            return 200, item
        except Exception as e:
            return 422, ErrorResponse(detail=str(e), code="UPDATE_ERROR")

    @router.delete(
        "/{item_id}/",
        response={204: None, 404: ErrorResponse, 503: ErrorResponse},
        summary=f"Delete {model.__name__}",
    )
    def delete_item(request: HttpRequest, item_id: int):
        """Delete an item."""
        error = check_media_crawl_enabled(request)
        if error:
            return 503, error

        try:
            item = model.objects.using("mysql").get(pk=item_id)
            item.delete(using="mysql")
            return 204, None
        except model.DoesNotExist:
            return 404, ErrorResponse(
                detail=f"{model.__name__} not found", code="NOT_FOUND"
            )

    @router.post(
        "/batch/",
        response={201: List[out_schema], 422: ErrorResponse, 503: ErrorResponse},
        summary=f"Batch create {model.__name__}",
    )
    def batch_create(request: HttpRequest, payload: List[create_schema]):
        """Create multiple items in batch."""
        error = check_media_crawl_enabled(request)
        if error:
            return 503, error

        try:
            items = [model(**item.dict()) for item in payload]
            created = model.objects.using("mysql").bulk_create(items)
            return 201, created
        except Exception as e:
            return 422, ErrorResponse(detail=str(e), code="BATCH_CREATE_ERROR")

    @router.delete(
        "/batch/",
        response={200: BatchDeleteResponse, 422: ErrorResponse, 503: ErrorResponse},
        summary=f"Batch delete {model.__name__}",
    )
    def batch_delete(request: HttpRequest, payload: BatchDeleteRequest):
        """Delete multiple items by IDs."""
        error = check_media_crawl_enabled(request)
        if error:
            return 503, error

        try:
            deleted_count, _ = (
                model.objects.using("mysql").filter(pk__in=payload.ids).delete()
            )
            return 200, BatchDeleteResponse(deleted_count=deleted_count)
        except Exception as e:
            return 422, ErrorResponse(detail=str(e), code="BATCH_DELETE_ERROR")

    return router

