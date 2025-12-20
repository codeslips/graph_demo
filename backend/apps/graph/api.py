"""
Django Ninja API routes for graph visualization.

Provides REST API endpoints for querying graph data from Neo4j.
"""

import logging
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router

from apps.crawl.models import CrawlTask
from services.neo4j_sync import get_popular_keywords, get_task_graph_data, search_nodes

from .schemas import (
    EdgeSchema,
    ErrorResponse,
    GraphDataResponse,
    GraphStatsSchema,
    KeywordListResponse,
    KeywordSchema,
    NodeSchema,
    SearchResponse,
    SearchResultSchema,
)

logger = logging.getLogger(__name__)

router = Router(tags=["Graph"])


@router.get(
    "/task/{task_id}",
    response={200: GraphDataResponse, 404: ErrorResponse},
    summary="Get graph data for a task",
)
def get_task_graph(request, task_id: UUID):
    """
    Get graph visualization data for a specific crawl task.

    Returns nodes (Articles, Channels, Tags) and edges (relationships)
    formatted for frontend graph rendering.
    """
    # Verify task exists
    task = get_object_or_404(CrawlTask, id=task_id)

    try:
        data = get_task_graph_data(str(task_id))

        # Transform to schema format
        nodes = [
            NodeSchema(
                id=n["id"],
                type=n["type"],
                label=n["label"],
                properties=n.get("properties", {}),
            )
            for n in data["nodes"]
        ]

        edges = [
            EdgeSchema(
                source=e["source"],
                target=e["target"],
                type=e["type"],
            )
            for e in data["edges"]
        ]

        stats = GraphStatsSchema(
            totalNodes=data["stats"]["totalNodes"],
            totalEdges=data["stats"]["totalEdges"],
            nodesByType=data["stats"]["nodesByType"],
        )

        return GraphDataResponse(nodes=nodes, edges=edges, stats=stats)

    except Exception as e:
        logger.error(f"Error fetching graph data: {e}")
        # Return empty graph on error
        return GraphDataResponse(
            nodes=[],
            edges=[],
            stats=GraphStatsSchema(totalNodes=0, totalEdges=0, nodesByType={}),
        )


@router.get(
    "/keywords",
    response=KeywordListResponse,
    summary="Get popular keywords/tags",
)
def get_keywords(request, limit: int = 50, task_id: str | None = None):
    """
    Get popular keywords/tags ordered by article count.

    Optionally filter by task_id to get keywords from a specific crawl.
    """
    try:
        keywords = get_popular_keywords(limit=limit, task_id=task_id)

        items = [
            KeywordSchema(
                tagId=k["tagId"],
                name=k["name"],
                count=k["count"],
            )
            for k in keywords
        ]

        return KeywordListResponse(items=items, total=len(items))

    except Exception as e:
        logger.error(f"Error fetching keywords: {e}")
        return KeywordListResponse(items=[], total=0)


@router.get(
    "/search",
    response=SearchResponse,
    summary="Search graph nodes",
)
def search_graph(request, q: str, limit: int = 20):
    """
    Search graph nodes by text.

    Matches against article titles and tag names.
    """
    if not q or len(q) < 2:
        return SearchResponse(items=[], total=0)

    try:
        results = search_nodes(query_text=q, limit=limit)

        items = [
            SearchResultSchema(
                id=r["id"],
                type=r["type"],
                label=r["label"],
                properties=r.get("properties", {}),
            )
            for r in results
        ]

        return SearchResponse(items=items, total=len(items))

    except Exception as e:
        logger.error(f"Error searching nodes: {e}")
        return SearchResponse(items=[], total=0)


# ============================================================================
# Media Graph Endpoints
# ============================================================================


@router.get(
    "/media",
    response=GraphDataResponse,
    summary="Get media graph data",
    tags=["Media Graph"],
)
def get_media_graph(
    request,
    platform: str | None = None,
    keyword: str | None = None,
    limit: int = 100,
):
    """
    Get graph visualization data for media content.

    Returns nodes (Platforms, Content, Keywords) and edges (relationships)
    formatted for frontend graph rendering.

    Args:
        platform: Filter by platform (bilibili, douyin, kuaishou, weibo, tieba, zhihu)
        keyword: Filter by keyword
        limit: Maximum nodes to return
    """
    from services.media_neo4j_sync import get_media_graph_data

    # Debug logging
    logger.info(f"get_media_graph called with platform={platform!r}, keyword={keyword!r}, limit={limit}")

    try:
        data = get_media_graph_data(platform=platform, keyword=keyword, limit=limit)
        logger.info(f"get_media_graph returned {len(data.get('nodes', []))} nodes, {len(data.get('edges', []))} edges")

        nodes = [
            NodeSchema(
                id=n["id"],
                type=n["type"],
                label=n["label"],
                properties=n.get("properties", {}),
            )
            for n in data["nodes"]
        ]

        edges = [
            EdgeSchema(
                source=e["source"],
                target=e["target"],
                type=e["type"],
            )
            for e in data["edges"]
        ]

        stats = GraphStatsSchema(
            totalNodes=data["stats"]["totalNodes"],
            totalEdges=data["stats"]["totalEdges"],
            nodesByType=data["stats"]["nodesByType"],
        )

        return GraphDataResponse(nodes=nodes, edges=edges, stats=stats)

    except Exception as e:
        logger.error(f"Error fetching media graph data: {e}")
        return GraphDataResponse(
            nodes=[],
            edges=[],
            stats=GraphStatsSchema(totalNodes=0, totalEdges=0, nodesByType={}),
        )


@router.get(
    "/media/keywords",
    response=KeywordListResponse,
    summary="Get popular media keywords",
    tags=["Media Graph"],
)
def get_media_keywords(request, platform: str | None = None, limit: int = 50):
    """
    Get popular keywords from media content.

    Optionally filter by platform.
    """
    from services.media_neo4j_sync import get_media_keywords as fetch_keywords

    try:
        keywords = fetch_keywords(platform=platform, limit=limit)

        # Use a generic format for media keywords (no tagId)
        items = [
            KeywordSchema(
                tagId=0,  # Media keywords don't have numeric IDs
                name=k["name"],
                count=k["count"],
            )
            for k in keywords
        ]

        return KeywordListResponse(items=items, total=len(items))

    except Exception as e:
        logger.error(f"Error fetching media keywords: {e}")
        return KeywordListResponse(items=[], total=0)


@router.get(
    "/media/search",
    response=SearchResponse,
    summary="Search media graph keywords",
    tags=["Media Graph"],
)
def search_media_graph(request, q: str, limit: int = 20):
    """
    Search keywords in media graph by text.

    Returns matching keywords with content counts.
    """
    from services.media_neo4j_sync import search_media_keywords

    if not q or len(q) < 2:
        return SearchResponse(items=[], total=0)

    try:
        results = search_media_keywords(query_text=q, limit=limit)

        items = [
            SearchResultSchema(
                id=f"keyword_{r['name']}",
                type="Keyword",
                label=r["name"],
                properties={"count": r["count"]},
            )
            for r in results
        ]

        return SearchResponse(items=items, total=len(items))

    except Exception as e:
        logger.error(f"Error searching media keywords: {e}")
        return SearchResponse(items=[], total=0)

