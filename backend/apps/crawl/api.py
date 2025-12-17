"""
Django Ninja API routes for crawl tasks.

Provides REST API endpoints for creating and managing crawl tasks.
"""

from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router

from .models import CrawlItem, CrawlTask
from .schemas import (
    CreateTaskRequest,
    CrawlItemResponse,
    ErrorResponse,
    ItemListResponse,
    TaskDetailResponse,
    TaskListResponse,
    TaskResponse,
)
from .tasks import execute_crawl_task

router = Router(tags=["Crawl Tasks"])


@router.post(
    "/tasks",
    response={201: TaskResponse, 400: ErrorResponse},
    summary="Create a new crawl task",
)
def create_task(request, payload: CreateTaskRequest):
    """
    Create a new crawl task and dispatch it for async execution.

    The task will be executed in the background by a Celery worker.
    """
    # Validate crawl_type
    valid_types = ["news_list", "article", "channel"]
    if payload.crawl_type not in valid_types:
        return 400, ErrorResponse(
            error="Invalid crawl type",
            detail=f"Must be one of: {', '.join(valid_types)}",
        )

    # Create task
    task = CrawlTask.objects.create(
        target_url=payload.target_url,
        crawl_type=payload.crawl_type,
    )

    # Dispatch Celery task
    execute_crawl_task.delay(str(task.id))

    return 201, TaskResponse.from_orm(task)


@router.get(
    "/tasks",
    response=TaskListResponse,
    summary="List all crawl tasks",
)
def list_tasks(request, page: int = 1, page_size: int = 20, status: str | None = None):
    """
    Get a paginated list of crawl tasks.

    Optionally filter by status: PENDING, RUNNING, DONE, FAILED
    """
    queryset = CrawlTask.objects.all()

    if status:
        queryset = queryset.filter(status=status.upper())

    total = queryset.count()

    # Pagination
    offset = (page - 1) * page_size
    tasks = queryset[offset : offset + page_size]

    return TaskListResponse(
        items=[TaskResponse.from_orm(t) for t in tasks],
        total=total,
        page=page,
        page_size=page_size,
        has_next=(offset + page_size) < total,
    )


@router.get(
    "/tasks/{task_id}",
    response={200: TaskDetailResponse, 404: ErrorResponse},
    summary="Get task details",
)
def get_task(request, task_id: UUID):
    """
    Get detailed information about a specific crawl task.
    """
    task = get_object_or_404(CrawlTask, id=task_id)

    return TaskDetailResponse(
        id=task.id,
        target_url=task.target_url,
        crawl_type=task.crawl_type,
        status=task.status,
        total_items=task.total_items,
        created_at=task.created_at,
        started_at=task.started_at,
        finished_at=task.finished_at,
        error_message=task.error_message,
        celery_task_id=task.celery_task_id,
    )


@router.delete(
    "/tasks/{task_id}",
    response={204: None, 404: ErrorResponse},
    summary="Delete a crawl task",
)
def delete_task(request, task_id: UUID):
    """
    Delete a crawl task and all its associated items.
    """
    task = get_object_or_404(CrawlTask, id=task_id)
    task.delete()
    return 204, None


@router.get(
    "/tasks/{task_id}/items",
    response={200: ItemListResponse, 404: ErrorResponse},
    summary="Get task items",
)
def get_task_items(request, task_id: UUID, page: int = 1, page_size: int = 50):
    """
    Get crawled items for a specific task.
    """
    task = get_object_or_404(CrawlTask, id=task_id)

    queryset = CrawlItem.objects.filter(task=task)
    total = queryset.count()

    # Pagination
    offset = (page - 1) * page_size
    items = queryset[offset : offset + page_size]

    return ItemListResponse(
        items=[CrawlItemResponse.from_orm(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )

