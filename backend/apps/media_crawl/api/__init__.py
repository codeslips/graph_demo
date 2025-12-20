# -*- coding: utf-8 -*-
"""Media Crawl API package - Main router."""

from typing import Optional

from ninja import Router, Schema

from .bilibili import router as bilibili_router
from .douyin import router as douyin_router
from .kuaishou import router as kuaishou_router
from .weibo import router as weibo_router
from .xhs import router as xhs_router
from .tieba import router as tieba_router
from .zhihu import router as zhihu_router

# Main media crawl router
router = Router(tags=["Media Crawl"])

# Mount platform-specific routers
router.add_router("/bilibili", bilibili_router)
router.add_router("/douyin", douyin_router)
router.add_router("/kuaishou", kuaishou_router)
router.add_router("/weibo", weibo_router)
router.add_router("/xhs", xhs_router)
router.add_router("/tieba", tieba_router)
router.add_router("/zhihu", zhihu_router)


# ============================================================================
# Schemas for Sync Endpoints
# ============================================================================


class SyncNeo4jRequest(Schema):
    """Request schema for Neo4j sync trigger."""

    platform: Optional[str] = None
    limit: Optional[int] = None
    sync: bool = False  # If True, run synchronously (for testing)


class SyncNeo4jResponse(Schema):
    """Response schema for Neo4j sync trigger."""

    task_id: Optional[str] = None
    message: str
    result: Optional[dict] = None  # For sync mode


class SyncStatusResponse(Schema):
    """Response schema for sync status."""

    status: str
    progress: int
    lastSyncTime: Optional[str] = None
    lastResult: Optional[dict] = None


class ErrorResponse(Schema):
    """Error response schema."""

    detail: str
    code: str


# ============================================================================
# API Endpoints
# ============================================================================


@router.get("/status", tags=["Media Crawl"])
def status(request):
    """Check media crawl API status."""
    from django.conf import settings

    return {
        "enabled": getattr(settings, "MEDIA_CRAWL_ENABLED", True),
        "integration_enabled": getattr(
            settings, "MEDIA_CRAWL_INTEGRATION_ENABLED", False
        ),
        "platforms": [
            "bilibili",
            "douyin",
            "kuaishou",
            "weibo",
            "xhs",
            "tieba",
            "zhihu",
        ],
    }


@router.post(
    "/sync-neo4j",
    response={200: SyncNeo4jResponse, 400: ErrorResponse, 503: ErrorResponse},
    tags=["Media Crawl"],
    summary="Trigger Neo4j sync for media data",
)
def trigger_sync_neo4j(request, payload: SyncNeo4jRequest = None):
    """
    Trigger sync of media data to Neo4j.

    Optionally specify a platform to sync only that platform's data.
    Set sync=True to run synchronously (for testing), otherwise runs as async Celery task.
    """
    from django.conf import settings

    from services.media_neo4j_sync import SUPPORTED_PLATFORMS, sync_platform_content

    # Check if media crawl is enabled
    if not getattr(settings, "MEDIA_CRAWL_ENABLED", True):
        return 503, ErrorResponse(
            detail="Media crawl feature is disabled",
            code="MEDIA_CRAWL_DISABLED",
        )

    # Validate platform if provided
    platform = payload.platform if payload else None
    limit = payload.limit if payload else None
    run_sync = payload.sync if payload else False

    if platform and platform not in SUPPORTED_PLATFORMS:
        return 400, ErrorResponse(
            detail=f"Unsupported platform: {platform}. Supported: {SUPPORTED_PLATFORMS}",
            code="INVALID_PLATFORM",
        )

    if run_sync:
        # Run synchronously (blocking) - useful for testing
        try:
            result = sync_platform_content(platform=platform, limit=limit)
            return 200, SyncNeo4jResponse(
                task_id=None,
                message=f"Sync completed for {'all platforms' if not platform else platform}",
                result=result,
            )
        except Exception as e:
            return 400, ErrorResponse(
                detail=f"Sync failed: {str(e)}",
                code="SYNC_ERROR",
            )
    else:
        # Trigger async Celery task
        from apps.media_crawl.tasks import sync_media_to_neo4j

        task = sync_media_to_neo4j.delay(platform=platform, limit=limit)

        return 200, SyncNeo4jResponse(
            task_id=task.id,
            message=f"Sync task started for {'all platforms' if not platform else platform}",
            result=None,
        )


@router.get(
    "/sync-status",
    response={200: SyncStatusResponse},
    tags=["Media Crawl"],
    summary="Get Neo4j sync status",
)
def get_sync_status(request):
    """
    Get current status of media Neo4j sync operation.

    Returns sync status, progress percentage, and last sync results.
    """
    from services.media_neo4j_sync import get_sync_status as get_status

    status_data = get_status()
    return 200, SyncStatusResponse(
        status=status_data.get("status", "idle"),
        progress=status_data.get("progress", 0),
        lastSyncTime=status_data.get("lastSyncTime"),
        lastResult=status_data.get("lastResult"),
    )
