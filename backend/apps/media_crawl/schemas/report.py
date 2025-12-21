# -*- coding: utf-8 -*-
"""Schemas for Analysis Report API."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ninja import Schema


class SourceKeywordsResponse(Schema):
    """Response schema for source keywords list."""

    keywords: List[str]


class ExportDataRequest(Schema):
    """Request schema for data export."""

    platform: str
    source_keyword: str
    time_from: Optional[int] = None
    time_to: Optional[int] = None


class ExportDataResponse(Schema):
    """Response schema for data export."""

    csv_data: str
    record_count: int
    truncated: bool = False
    total_count: int = 0


class ReportCreateRequest(Schema):
    """Request schema for creating a report."""

    title: str
    platform: str
    source_keyword: str
    time_from: Optional[int] = None
    time_to: Optional[int] = None
    content: str
    record_count: int = 0


class ReportSchema(Schema):
    """Response schema for a single report."""

    id: UUID
    title: str
    platform: str
    source_keyword: str
    time_from: Optional[int] = None
    time_to: Optional[int] = None
    content: str
    record_count: int
    created_at: datetime


class ReportListItemSchema(Schema):
    """Response schema for report list item (without content)."""

    id: UUID
    title: str
    platform: str
    source_keyword: str
    time_from: Optional[int] = None
    time_to: Optional[int] = None
    record_count: int
    created_at: datetime


class ReportListResponse(Schema):
    """Paginated response for report list."""

    items: List[ReportListItemSchema]
    total: int
    limit: int
    offset: int


class ReportErrorResponse(Schema):
    """Error response for report endpoints."""

    detail: str
    code: str

