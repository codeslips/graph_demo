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
from .report import router as report_router

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
router.add_router("/reports", report_router)


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


# ============================================================================
# External Crawler Service Proxy Endpoints
# ============================================================================

from apps.media_crawl.schemas import (
    CrawlerStartRequest,
    CrawlerStartResponse,
    CrawlerStatusResponse,
    CrawlerErrorResponse,
)


@router.post(
    "/crawler/start",
    response={200: CrawlerStartResponse, 503: CrawlerErrorResponse},
    tags=["Media Crawler"],
    summary="Start a new crawler task",
)
def start_crawler_task(request, payload: CrawlerStartRequest):
    """
    Start a new crawler task via the external media crawl service.

    Proxies the request to the external crawler service configured via
    MEDIA_CRAWL_SERVICE_URL environment variable.
    """
    import httpx
    from django.conf import settings

    # Check if media crawl is enabled
    if not getattr(settings, "MEDIA_CRAWL_ENABLED", True):
        return 503, CrawlerErrorResponse(
            detail="Media crawl feature is disabled",
            code="MEDIA_CRAWL_DISABLED",
        )

    service_url = getattr(settings, "MEDIA_CRAWL_SERVICE_URL", "http://localhost:8777")
    endpoint = f"{service_url}/api/crawler/start"

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                endpoint,
                json=payload.dict(),
            )
            response.raise_for_status()
            return 200, CrawlerStartResponse(
                success=True,
                message="Crawler task started successfully",
            )
    except httpx.ConnectError:
        return 503, CrawlerErrorResponse(
            detail=f"Cannot connect to crawler service at {service_url}",
            code="SERVICE_UNAVAILABLE",
        )
    except httpx.TimeoutException:
        return 503, CrawlerErrorResponse(
            detail="Crawler service request timed out",
            code="SERVICE_TIMEOUT",
        )
    except httpx.HTTPStatusError as e:
        return 503, CrawlerErrorResponse(
            detail=f"Crawler service error: {e.response.text}",
            code="SERVICE_ERROR",
        )
    except Exception as e:
        return 503, CrawlerErrorResponse(
            detail=f"Unexpected error: {str(e)}",
            code="UNEXPECTED_ERROR",
        )


@router.get(
    "/crawler/status",
    response={200: CrawlerStatusResponse, 503: CrawlerErrorResponse},
    tags=["Media Crawler"],
    summary="Get current crawler task status",
)
def get_crawler_status(request):
    """
    Get the current status of the crawler task from the external service.

    Proxies the request to the external crawler service configured via
    MEDIA_CRAWL_SERVICE_URL environment variable.
    """
    import httpx
    from django.conf import settings

    # Check if media crawl is enabled
    if not getattr(settings, "MEDIA_CRAWL_ENABLED", True):
        return 503, CrawlerErrorResponse(
            detail="Media crawl feature is disabled",
            code="MEDIA_CRAWL_DISABLED",
        )

    service_url = getattr(settings, "MEDIA_CRAWL_SERVICE_URL", "http://localhost:8777")
    endpoint = f"{service_url}/api/crawler/status"

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(endpoint)
            response.raise_for_status()
            data = response.json()
            return 200, CrawlerStatusResponse(
                status=data.get("status", "idle"),
                platform=data.get("platform"),
                crawler_type=data.get("crawler_type"),
                started_at=data.get("started_at"),
                error_message=data.get("error_message"),
            )
    except httpx.ConnectError:
        return 503, CrawlerErrorResponse(
            detail=f"Cannot connect to crawler service at {service_url}",
            code="SERVICE_UNAVAILABLE",
        )
    except httpx.TimeoutException:
        return 503, CrawlerErrorResponse(
            detail="Crawler service request timed out",
            code="SERVICE_TIMEOUT",
        )
    except httpx.HTTPStatusError as e:
        return 503, CrawlerErrorResponse(
            detail=f"Crawler service error: {e.response.text}",
            code="SERVICE_ERROR",
        )
    except Exception as e:
        return 503, CrawlerErrorResponse(
            detail=f"Unexpected error: {str(e)}",
            code="UNEXPECTED_ERROR",
        )
