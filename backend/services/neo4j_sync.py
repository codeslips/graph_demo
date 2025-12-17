"""
Neo4j data synchronization service.

Syncs crawled data from PostgreSQL to Neo4j as graph nodes and relationships.
"""

import logging
from typing import Any
from uuid import UUID

from apps.crawl.models import CrawlItem, CrawlTask
from services.neo4j_client import get_neo4j_client

logger = logging.getLogger(__name__)

# Cypher queries for node creation
MERGE_WEBSITE_QUERY = """
MERGE (w:Website {domain: $domain})
SET w.name = $name
RETURN w
"""

MERGE_CHANNEL_QUERY = """
MERGE (c:Channel {nodeId: $nodeId})
SET c.name = $name, c.desc = $desc
WITH c
MATCH (w:Website {domain: 'thepaper.cn'})
MERGE (w)-[:HAS_CHANNEL]->(c)
RETURN c
"""

MERGE_ARTICLE_QUERY = """
MERGE (a:Article {contId: $contId})
SET a.title = $title,
    a.author = $author,
    a.url = $url,
    a.summary = $summary,
    a.pubTime = $pubTime,
    a.taskId = $taskId
WITH a
MATCH (c:Channel {nodeId: $channelId})
MERGE (c)-[:CONTAINS]->(a)
RETURN a
"""

MERGE_TAG_QUERY = """
MERGE (t:Tag {tagId: $tagId})
SET t.name = $name
WITH t
MATCH (a:Article {contId: $contId})
MERGE (a)-[:HAS_TAG]->(t)
RETURN t
"""


def sync_task_to_neo4j(task_id: str | UUID) -> dict[str, Any]:
    """
    Sync all items from a CrawlTask to Neo4j.

    Args:
        task_id: UUID of the CrawlTask

    Returns:
        Summary of sync operation
    """
    logger.info(f"Starting Neo4j sync for task {task_id}")

    client = get_neo4j_client()

    # Get items that haven't been synced yet
    items = CrawlItem.objects.filter(
        task_id=task_id,
        neo4j_synced=False,
    ).select_related("task")

    if not items.exists():
        logger.info(f"No items to sync for task {task_id}")
        return {"items_synced": 0, "task_id": str(task_id)}

    # Ensure Website node exists
    _ensure_website_node(client)

    # Track unique channels to sync
    channels_synced: set[int] = set()
    items_synced = 0
    tags_synced = 0

    with client.session() as session:
        for item in items:
            try:
                # Sync channel if not already done
                if item.channel_id and item.channel_id not in channels_synced:
                    _sync_channel(session, item.channel_id, item.channel_name)
                    channels_synced.add(item.channel_id)

                # Sync article
                _sync_article(session, item)

                # Sync tags
                for tag in item.tags:
                    if tag.get("tagId") and tag.get("tag"):
                        _sync_tag(session, item.cont_id, tag)
                        tags_synced += 1

                # Mark item as synced
                item.neo4j_synced = True
                item.save(update_fields=["neo4j_synced"])
                items_synced += 1

            except Exception as e:
                logger.error(f"Error syncing item {item.cont_id}: {e}")
                continue

    logger.info(
        f"Neo4j sync completed for task {task_id}: "
        f"{items_synced} items, {len(channels_synced)} channels, {tags_synced} tags"
    )

    return {
        "task_id": str(task_id),
        "items_synced": items_synced,
        "channels_synced": len(channels_synced),
        "tags_synced": tags_synced,
    }


def _ensure_website_node(client) -> None:
    """Ensure the ThePaper website node exists."""
    client.run_write_query(
        MERGE_WEBSITE_QUERY,
        {"domain": "thepaper.cn", "name": "澎湃新闻"},
    )


def _sync_channel(session, channel_id: int, channel_name: str) -> None:
    """Sync a channel node to Neo4j."""
    session.run(
        MERGE_CHANNEL_QUERY,
        {
            "nodeId": channel_id,
            "name": channel_name,
            "desc": "",
        },
    )


def _sync_article(session, item: CrawlItem) -> None:
    """Sync an article node to Neo4j."""
    pub_time = item.publish_time.isoformat() if item.publish_time else ""

    session.run(
        MERGE_ARTICLE_QUERY,
        {
            "contId": item.cont_id,
            "title": item.title,
            "author": item.author,
            "url": item.url,
            "summary": item.summary[:500] if item.summary else "",
            "pubTime": pub_time,
            "taskId": str(item.task_id),
            "channelId": item.channel_id,
        },
    )


def _sync_tag(session, cont_id: str, tag: dict[str, Any]) -> None:
    """Sync a tag node and relationship to Neo4j."""
    session.run(
        MERGE_TAG_QUERY,
        {
            "tagId": tag["tagId"],
            "name": tag["tag"],
            "contId": cont_id,
        },
    )


def get_task_graph_data(task_id: str | UUID) -> dict[str, Any]:
    """
    Fetch graph data for a specific task from Neo4j.

    Args:
        task_id: UUID of the CrawlTask

    Returns:
        Graph data with nodes and edges
    """
    client = get_neo4j_client()

    # Query for articles, channels, and tags related to this task
    query = """
    MATCH (c:Channel)-[:CONTAINS]->(a:Article {taskId: $taskId})
    OPTIONAL MATCH (a)-[:HAS_TAG]->(t:Tag)
    RETURN c, a, collect(DISTINCT t) as tags
    """

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    node_ids: set[str] = set()

    with client.session() as session:
        result = session.run(query, {"taskId": str(task_id)})

        for record in result:
            channel = record.get("c")
            article = record.get("a")
            tags = record.get("tags", [])

            # Add channel node
            if channel:
                channel_id = f"channel_{channel.get('nodeId')}"
                if channel_id not in node_ids:
                    nodes.append({
                        "id": channel_id,
                        "type": "Channel",
                        "label": channel.get("name", "Unknown"),
                        "properties": dict(channel),
                    })
                    node_ids.add(channel_id)

            # Add article node
            if article:
                article_id = f"article_{article.get('contId')}"
                if article_id not in node_ids:
                    nodes.append({
                        "id": article_id,
                        "type": "Article",
                        "label": article.get("title", "")[:50],
                        "properties": dict(article),
                    })
                    node_ids.add(article_id)

                    # Add CONTAINS edge
                    if channel:
                        channel_id = f"channel_{channel.get('nodeId')}"
                        edges.append({
                            "source": channel_id,
                            "target": article_id,
                            "type": "CONTAINS",
                        })

                # Add tag nodes and edges
                for tag in tags:
                    if tag:
                        tag_id = f"tag_{tag.get('tagId')}"
                        if tag_id not in node_ids:
                            nodes.append({
                                "id": tag_id,
                                "type": "Tag",
                                "label": tag.get("name", ""),
                                "properties": dict(tag),
                            })
                            node_ids.add(tag_id)

                        edges.append({
                            "source": article_id,
                            "target": tag_id,
                            "type": "HAS_TAG",
                        })

    # Calculate stats
    stats = {
        "totalNodes": len(nodes),
        "totalEdges": len(edges),
        "nodesByType": {},
    }
    for node in nodes:
        node_type = node["type"]
        stats["nodesByType"][node_type] = stats["nodesByType"].get(node_type, 0) + 1

    return {
        "nodes": nodes,
        "edges": edges,
        "stats": stats,
    }


def get_popular_keywords(limit: int = 50, task_id: str | None = None) -> list[dict[str, Any]]:
    """
    Get popular tags/keywords ordered by article count.

    Args:
        limit: Maximum number of keywords to return
        task_id: Optional task ID to filter by

    Returns:
        List of keywords with counts
    """
    client = get_neo4j_client()

    if task_id:
        query = """
        MATCH (a:Article {taskId: $taskId})-[:HAS_TAG]->(t:Tag)
        RETURN t.tagId as tagId, t.name as name, count(a) as count
        ORDER BY count DESC
        LIMIT $limit
        """
        params = {"taskId": str(task_id), "limit": limit}
    else:
        query = """
        MATCH (a:Article)-[:HAS_TAG]->(t:Tag)
        RETURN t.tagId as tagId, t.name as name, count(a) as count
        ORDER BY count DESC
        LIMIT $limit
        """
        params = {"limit": limit}

    return client.run_query(query, params)


def search_nodes(query_text: str, limit: int = 20) -> list[dict[str, Any]]:
    """
    Search nodes by text matching article titles and tag names.

    Args:
        query_text: Search query
        limit: Maximum results to return

    Returns:
        List of matching nodes
    """
    client = get_neo4j_client()

    # Use case-insensitive contains search
    query = """
    CALL {
        MATCH (a:Article)
        WHERE toLower(a.title) CONTAINS toLower($query)
        RETURN a.contId as id, 'Article' as type, a.title as label, a as node
        UNION
        MATCH (t:Tag)
        WHERE toLower(t.name) CONTAINS toLower($query)
        RETURN toString(t.tagId) as id, 'Tag' as type, t.name as label, t as node
    }
    RETURN id, type, label, properties(node) as properties
    LIMIT $limit
    """

    results = client.run_query(query, {"query": query_text, "limit": limit})

    return [
        {
            "id": r["id"],
            "type": r["type"],
            "label": r["label"],
            "properties": r["properties"],
        }
        for r in results
    ]

