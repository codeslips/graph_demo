# -*- coding: utf-8 -*-
"""Analysis Report API endpoints."""

from typing import Optional
from uuid import UUID

from django.conf import settings
from django.http import HttpRequest
from ninja import Router

from ..models import (
    AnalysisReport,
    XhsNote,
    DouyinAweme,
    WeiboNote,
    BilibiliVideo,
    KuaishouVideo,
    TiebaNote,
    ZhihuContent,
)
from ..schemas.report import (
    ExportDataRequest,
    ExportDataResponse,
    ReportCreateRequest,
    ReportErrorResponse,
    ReportListItemSchema,
    ReportListResponse,
    ReportSchema,
    SourceKeywordsResponse,
)

router = Router(tags=["Analysis Reports"])

# Platform model mapping
PLATFORM_MODELS = {
    "xhs": XhsNote,
    "douyin": DouyinAweme,
    "weibo": WeiboNote,
    "bilibili": BilibiliVideo,
    "kuaishou": KuaishouVideo,
    "tieba": TiebaNote,
    "zhihu": ZhihuContent,
}

# Platform time field mapping
PLATFORM_TIME_FIELDS = {
    "xhs": "time",
    "douyin": "create_time",
    "weibo": "create_time",
    "bilibili": "create_time",
    "kuaishou": "create_time",
    "tieba": "publish_time",
    "zhihu": "created_time",
}

# Platform export fields mapping
PLATFORM_EXPORT_FIELDS = {
    "xhs": [
        "note_id", "title", "desc", "liked_count", "collected_count",
        "comment_count", "share_count", "time", "user_id", "nickname",
        "ip_location", "tag_list"
    ],
    "douyin": [
        "aweme_id", "title", "desc", "liked_count", "collected_count",
        "comment_count", "share_count", "create_time", "user_id", "nickname",
        "ip_location", "tag_list"
    ],
    "weibo": [
        "note_id", "content", "liked_count", "comments_count",
        "share_count", "create_time", "user_id", "nickname", "ip_location"
    ],
    "bilibili": [
        "video_id", "title", "desc", "view_count", "coin_count",
        "danmaku_count", "create_time", "user_id", "nickname"
    ],
    "kuaishou": [
        "video_id", "title", "desc", "view_count", "liked_count",
        "comment_count", "create_time", "user_id", "nickname"
    ],
    "tieba": [
        "note_id", "title", "content", "reply_count", "share_count",
        "publish_time", "user_id", "user_nickname", "tieba_name"
    ],
    "zhihu": [
        "content_id", "title", "content", "voteup_count", "comment_count",
        "created_time", "user_id", "user_nickname", "content_type"
    ],
}

MAX_EXPORT_RECORDS = 500


def check_media_crawl_enabled() -> Optional[ReportErrorResponse]:
    """Check if media crawl feature is enabled."""
    if not getattr(settings, "MEDIA_CRAWL_ENABLED", True):
        return ReportErrorResponse(
            detail="Media crawl feature is disabled",
            code="MEDIA_CRAWL_DISABLED",
        )
    return None


@router.get(
    "/source-keywords/",
    response={200: SourceKeywordsResponse, 400: ReportErrorResponse, 503: ReportErrorResponse},
    summary="Get unique source keywords for a platform",
)
def get_source_keywords(request: HttpRequest, platform: str):
    """Get list of unique source_keyword values from a platform's content."""
    error = check_media_crawl_enabled()
    if error:
        return 503, error

    if platform not in PLATFORM_MODELS:
        return 400, ReportErrorResponse(
            detail=f"Unsupported platform: {platform}. Supported: {list(PLATFORM_MODELS.keys())}",
            code="INVALID_PLATFORM",
        )

    model = PLATFORM_MODELS[platform]

    # Check if model has source_keyword field
    field_names = [f.name for f in model._meta.get_fields()]
    if "source_keyword" not in field_names:
        return 200, SourceKeywordsResponse(keywords=[])

    # Get unique non-empty source_keywords
    keywords = (
        model.objects.using("mysql")
        .exclude(source_keyword="")
        .exclude(source_keyword__isnull=True)
        .values_list("source_keyword", flat=True)
        .distinct()
        .order_by("source_keyword")
    )

    return 200, SourceKeywordsResponse(keywords=list(keywords))


@router.post(
    "/export-data/",
    response={200: ExportDataResponse, 400: ReportErrorResponse, 404: ReportErrorResponse, 503: ReportErrorResponse},
    summary="Export filtered media data as CSV-like text",
)
def export_data(request: HttpRequest, payload: ExportDataRequest):
    """Export media data filtered by source_keyword and time range."""
    error = check_media_crawl_enabled()
    if error:
        return 503, error

    platform = payload.platform
    if platform not in PLATFORM_MODELS:
        return 400, ReportErrorResponse(
            detail=f"Unsupported platform: {platform}",
            code="INVALID_PLATFORM",
        )

    model = PLATFORM_MODELS[platform]
    time_field = PLATFORM_TIME_FIELDS.get(platform, "create_time")
    export_fields = PLATFORM_EXPORT_FIELDS.get(platform, [])

    # Build query
    queryset = model.objects.using("mysql").all()

    # Filter by source_keyword
    field_names = [f.name for f in model._meta.get_fields()]
    if "source_keyword" in field_names:
        queryset = queryset.filter(source_keyword=payload.source_keyword)
    else:
        # For platforms without source_keyword, return error
        return 400, ReportErrorResponse(
            detail=f"Platform {platform} does not support source_keyword filtering",
            code="NO_SOURCE_KEYWORD",
        )

    # Check if any records exist with this keyword
    if not queryset.exists():
        return 404, ReportErrorResponse(
            detail=f"No records found for source_keyword: {payload.source_keyword}",
            code="KEYWORD_NOT_FOUND",
        )

    # Filter by time range
    # Note: Database stores timestamps in milliseconds, but API receives seconds
    if payload.time_from and time_field in field_names:
        time_from_ms = payload.time_from * 1000  # Convert seconds to milliseconds
        queryset = queryset.filter(**{f"{time_field}__gte": time_from_ms})
    if payload.time_to and time_field in field_names:
        time_to_ms = payload.time_to * 1000  # Convert seconds to milliseconds
        queryset = queryset.filter(**{f"{time_field}__lte": time_to_ms})

    total_count = queryset.count()
    truncated = total_count > MAX_EXPORT_RECORDS

    # Limit records
    records = queryset[:MAX_EXPORT_RECORDS]

    # Build CSV-like output
    lines = [",".join(export_fields)]  # Header

    for record in records:
        row = []
        for field in export_fields:
            value = getattr(record, field, "")
            if value is None:
                value = ""
            # Escape commas and quotes in string values
            str_value = str(value).replace('"', '""')
            if "," in str_value or '"' in str_value or "\n" in str_value:
                str_value = f'"{str_value}"'
            row.append(str_value)
        lines.append(",".join(row))

    csv_data = "\n".join(lines)

    return 200, ExportDataResponse(
        csv_data=csv_data,
        record_count=len(records),
        truncated=truncated,
        total_count=total_count,
    )


@router.post(
    "/",
    response={201: ReportSchema, 422: ReportErrorResponse, 503: ReportErrorResponse},
    summary="Create a new analysis report",
)
def create_report(request: HttpRequest, payload: ReportCreateRequest):
    """Create and save a new analysis report."""
    error = check_media_crawl_enabled()
    if error:
        return 503, error

    try:
        # Use default PostgreSQL database (not MySQL)
        report = AnalysisReport.objects.using('default').create(
            title=payload.title,
            platform=payload.platform,
            source_keyword=payload.source_keyword,
            time_from=payload.time_from,
            time_to=payload.time_to,
            content=payload.content,
            record_count=payload.record_count,
        )
        return 201, report
    except Exception as e:
        return 422, ReportErrorResponse(
            detail=str(e),
            code="CREATE_ERROR",
        )


@router.get(
    "/",
    response={200: ReportListResponse, 503: ReportErrorResponse},
    summary="List all analysis reports",
)
def list_reports(
    request: HttpRequest,
    limit: int = 20,
    offset: int = 0,
    platform: Optional[str] = None,
):
    """Get paginated list of analysis reports."""
    error = check_media_crawl_enabled()
    if error:
        return 503, error

    # Use default PostgreSQL database (not MySQL)
    queryset = AnalysisReport.objects.using('default').all()

    if platform:
        queryset = queryset.filter(platform=platform)

    total = queryset.count()
    items = list(queryset[offset : offset + limit])

    return 200, ReportListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{report_id}/",
    response={200: ReportSchema, 404: ReportErrorResponse, 503: ReportErrorResponse},
    summary="Get a single analysis report",
)
def get_report(request: HttpRequest, report_id: UUID):
    """Get a single report by ID."""
    error = check_media_crawl_enabled()
    if error:
        return 503, error

    try:
        # Use default PostgreSQL database (not MySQL)
        report = AnalysisReport.objects.using('default').get(pk=report_id)
        return 200, report
    except AnalysisReport.DoesNotExist:
        return 404, ReportErrorResponse(
            detail="Report not found",
            code="NOT_FOUND",
        )


@router.delete(
    "/{report_id}/",
    response={204: None, 404: ReportErrorResponse, 503: ReportErrorResponse},
    summary="Delete an analysis report",
)
def delete_report(request: HttpRequest, report_id: UUID):
    """Delete a report by ID."""
    error = check_media_crawl_enabled()
    if error:
        return 503, error

    try:
        # Use default PostgreSQL database (not MySQL)
        report = AnalysisReport.objects.using('default').get(pk=report_id)
        report.delete()
        return 204, None
    except AnalysisReport.DoesNotExist:
        return 404, ReportErrorResponse(
            detail="Report not found",
            code="NOT_FOUND",
        )

