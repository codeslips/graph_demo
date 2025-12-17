"""
Django Ninja schemas for graph API.

Request and response schemas for graph visualization endpoints.
"""

from typing import Any

from ninja import Schema


class NodeSchema(Schema):
    """Schema for a graph node."""

    id: str
    type: str
    label: str
    properties: dict[str, Any] = {}


class EdgeSchema(Schema):
    """Schema for a graph edge."""

    source: str
    target: str
    type: str


class GraphStatsSchema(Schema):
    """Schema for graph statistics."""

    totalNodes: int
    totalEdges: int
    nodesByType: dict[str, int]


class GraphDataResponse(Schema):
    """Response schema for graph data."""

    nodes: list[NodeSchema]
    edges: list[EdgeSchema]
    stats: GraphStatsSchema


class KeywordSchema(Schema):
    """Schema for a keyword/tag."""

    tagId: int
    name: str
    count: int


class KeywordListResponse(Schema):
    """Response schema for keyword list."""

    items: list[KeywordSchema]
    total: int


class SearchResultSchema(Schema):
    """Schema for search result item."""

    id: str
    type: str
    label: str
    properties: dict[str, Any] = {}


class SearchResponse(Schema):
    """Response schema for search results."""

    items: list[SearchResultSchema]
    total: int


class ErrorResponse(Schema):
    """Error response schema."""

    error: str
    detail: str = ""

