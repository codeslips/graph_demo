"""
Media data Neo4j synchronization service.

Syncs media platform data (Bilibili, Douyin, Kuaishou, Weibo, XHS, Tieba, Zhihu)
from MySQL to Neo4j as a content-centric graph model.

Graph Model:
    (:Platform {name}) -[:HAS_CONTENT]-> (:Content {contentId, platform, ...})
    (:Content) -[:HAS_KEYWORD]-> (:Keyword {name})
    (:Content) -[:HAS_COMMENT]-> (:Comment {commentId, ...})
"""

import logging
import re
from datetime import datetime
from typing import Any

from django.core.cache import cache

from services.neo4j_client import get_neo4j_client

# Import neo4j time types for serialization
try:
    from neo4j.time import DateTime as Neo4jDateTime, Date as Neo4jDate, Time as Neo4jTime
    NEO4J_TIME_TYPES = (Neo4jDateTime, Neo4jDate, Neo4jTime)
except ImportError:
    NEO4J_TIME_TYPES = ()

logger = logging.getLogger(__name__)

# Supported platforms (all 7 platforms)
SUPPORTED_PLATFORMS = ["bilibili", "douyin", "kuaishou", "weibo", "xhs", "tieba", "zhihu"]

# Cache key for sync status
SYNC_STATUS_CACHE_KEY = "media_neo4j_sync_status"

# ============================================================================
# Cypher Queries
# ============================================================================

MERGE_PLATFORM_QUERY = """
MERGE (p:MediaPlatform {name: $name})
SET p.displayName = $displayName,
    p.updatedAt = datetime()
RETURN p
"""

MERGE_CONTENT_QUERY = """
MERGE (c:MediaContent {contentId: $contentId, platform: $platform})
SET c.contentType = $contentType,
    c.title = $title,
    c.author = $author,
    c.authorId = $authorId,
    c.url = $url,
    c.createTime = $createTime,
    c.likedCount = $likedCount,
    c.commentCount = $commentCount,
    c.syncedAt = datetime()
WITH c
MATCH (p:MediaPlatform {name: $platform})
MERGE (p)-[:HAS_CONTENT]->(c)
RETURN c
"""

MERGE_KEYWORD_QUERY = """
MERGE (k:MediaKeyword {name: $name})
WITH k
MATCH (c:MediaContent {contentId: $contentId, platform: $platform})
MERGE (c)-[:HAS_KEYWORD]->(k)
RETURN k
"""

MERGE_COMMENT_QUERY = """
MERGE (cm:MediaComment {commentId: $commentId, platform: $platform})
SET cm.content = $content,
    cm.author = $author,
    cm.authorId = $authorId,
    cm.createTime = $createTime,
    cm.likedCount = $likedCount
WITH cm
MATCH (c:MediaContent {contentId: $contentId, platform: $platform})
MERGE (c)-[:HAS_COMMENT]->(cm)
RETURN cm
"""

# Graph data retrieval queries
GET_MEDIA_GRAPH_BY_PLATFORM_QUERY = """
MATCH (p:MediaPlatform {name: $platform})-[:HAS_CONTENT]->(c:MediaContent)
OPTIONAL MATCH (c)-[:HAS_KEYWORD]->(k:MediaKeyword)
OPTIONAL MATCH (c)-[:HAS_COMMENT]->(cm:MediaComment)
RETURN p, c, collect(DISTINCT k) as keywords, count(DISTINCT cm) as commentCount
LIMIT $limit
"""

GET_MEDIA_GRAPH_ALL_PLATFORMS_QUERY = """
MATCH (p:MediaPlatform)-[:HAS_CONTENT]->(c:MediaContent)
OPTIONAL MATCH (c)-[:HAS_KEYWORD]->(k:MediaKeyword)
OPTIONAL MATCH (c)-[:HAS_COMMENT]->(cm:MediaComment)
RETURN p, c, collect(DISTINCT k) as keywords, count(DISTINCT cm) as commentCount
LIMIT $limit
"""

GET_MEDIA_GRAPH_BY_KEYWORD_QUERY = """
MATCH (k:MediaKeyword)<-[:HAS_KEYWORD]-(c:MediaContent)<-[:HAS_CONTENT]-(p:MediaPlatform)
WHERE toLower(k.name) = toLower($keyword)
OPTIONAL MATCH (c)-[:HAS_KEYWORD]->(k2:MediaKeyword)
OPTIONAL MATCH (c)-[:HAS_COMMENT]->(cm:MediaComment)
RETURN p, c, collect(DISTINCT k2) as keywords, count(DISTINCT cm) as commentCount
LIMIT $limit
"""

GET_MEDIA_GRAPH_BY_PLATFORM_AND_KEYWORD_QUERY = """
MATCH (k:MediaKeyword)<-[:HAS_KEYWORD]-(c:MediaContent {platform: $platform})<-[:HAS_CONTENT]-(p:MediaPlatform)
WHERE toLower(k.name) = toLower($keyword)
OPTIONAL MATCH (c)-[:HAS_KEYWORD]->(k2:MediaKeyword)
OPTIONAL MATCH (c)-[:HAS_COMMENT]->(cm:MediaComment)
RETURN p, c, collect(DISTINCT k2) as keywords, count(DISTINCT cm) as commentCount
LIMIT $limit
"""

GET_POPULAR_KEYWORDS_ALL_QUERY = """
MATCH (c:MediaContent)-[:HAS_KEYWORD]->(k:MediaKeyword)
RETURN k.name as name, count(c) as count
ORDER BY count DESC
LIMIT $limit
"""

GET_POPULAR_KEYWORDS_BY_PLATFORM_QUERY = """
MATCH (c:MediaContent {platform: $platform})-[:HAS_KEYWORD]->(k:MediaKeyword)
RETURN k.name as name, count(c) as count
ORDER BY count DESC
LIMIT $limit
"""

SEARCH_KEYWORDS_QUERY = """
MATCH (k:MediaKeyword)
WHERE toLower(k.name) CONTAINS toLower($query)
OPTIONAL MATCH (c:MediaContent)-[:HAS_KEYWORD]->(k)
RETURN k.name as name, count(c) as count
ORDER BY count DESC
LIMIT $limit
"""


# ============================================================================
# Keyword Extraction
# ============================================================================

def extract_keywords(
    source_keyword: str | None,
    title: str | None,
    desc: str | None,
    tag_list: str | None = None,
) -> list[str]:
    """
    Extract keywords from content fields.

    Extraction sources:
    - source_keyword field (if non-empty)
    - Hashtags in title/desc (pattern: #keyword# or #keyword followed by space/end)
    - tag_list field (comma-separated or JSON-like)

    Args:
        source_keyword: Source keyword field
        title: Content title
        desc: Content description
        tag_list: Tag list field (platform-specific format)

    Returns:
        List of unique keywords (normalized: lowercase, trimmed)
    """
    keywords: set[str] = set()

    # Extract from source_keyword
    if source_keyword and source_keyword.strip():
        keywords.add(source_keyword.strip().lower())

    # Extract hashtags from title and desc
    text = f"{title or ''} {desc or ''}"
    # Pattern: #keyword# or #keyword followed by space/punctuation/end
    hashtag_pattern = r"#([^#\s]+)#|#([^\s#]+)"
    matches = re.findall(hashtag_pattern, text)
    for match in matches:
        tag = match[0] or match[1]
        if tag and len(tag) <= 50:  # Skip overly long matches
            keywords.add(tag.strip().lower())

    # Extract from tag_list (handle various formats)
    if tag_list and tag_list.strip():
        # Try splitting by common delimiters
        for delimiter in [",", ";", "|", "、"]:
            if delimiter in tag_list:
                for tag in tag_list.split(delimiter):
                    tag = tag.strip().strip('"').strip("'")
                    if tag and len(tag) <= 50:
                        keywords.add(tag.lower())
                break
        else:
            # Single tag or unknown format
            tag = tag_list.strip()
            if tag and len(tag) <= 50:
                keywords.add(tag.lower())

    return list(keywords)


# ============================================================================
# Platform Sync Functions
# ============================================================================

def _ensure_platform_node(client, platform: str, display_name: str) -> None:
    """Ensure platform node exists in Neo4j."""
    client.run_write_query(
        MERGE_PLATFORM_QUERY,
        {"name": platform, "displayName": display_name},
    )


def _sync_content_node(session, content_data: dict[str, Any]) -> None:
    """Sync a content node to Neo4j."""
    session.run(MERGE_CONTENT_QUERY, content_data)


def _sync_keyword_nodes(session, content_id: str, platform: str, keywords: list[str]) -> int:
    """Sync keyword nodes and relationships."""
    synced = 0
    for keyword in keywords:
        if keyword:
            session.run(
                MERGE_KEYWORD_QUERY,
                {"name": keyword, "contentId": content_id, "platform": platform},
            )
            synced += 1
    return synced


def _sync_comment_node(session, comment_data: dict[str, Any]) -> None:
    """Sync a comment node to Neo4j."""
    session.run(MERGE_COMMENT_QUERY, comment_data)


def _safe_int(value: Any, default: int = 0) -> int:
    """Safely convert value to int."""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def _safe_str(value: Any, default: str = "") -> str:
    """Safely convert value to string."""
    if value is None:
        return default
    return str(value)


def _timestamp_to_iso(ts: int | None) -> str:
    """Convert Unix timestamp to ISO string."""
    if ts is None or ts == 0:
        return ""
    try:
        return datetime.fromtimestamp(ts).isoformat()
    except (ValueError, OSError):
        return ""


def _serialize_neo4j_value(value: Any) -> Any:
    """Convert Neo4j types to JSON-serializable values."""
    if value is None:
        return None
    if NEO4J_TIME_TYPES and isinstance(value, NEO4J_TIME_TYPES):
        return value.iso_format()
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, (list, tuple)):
        return [_serialize_neo4j_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _serialize_neo4j_value(v) for k, v in value.items()}
    return value


def _serialize_node_properties(node) -> dict[str, Any]:
    """Convert Neo4j node to a JSON-serializable dict."""
    if node is None:
        return {}
    return {k: _serialize_neo4j_value(v) for k, v in dict(node).items()}


# ============================================================================
# Platform-Specific Sync Implementations
# ============================================================================

def sync_bilibili_content(limit: int | None = None) -> dict[str, int]:
    """Sync Bilibili videos and comments to Neo4j."""
    from apps.media_crawl.models import BilibiliVideo, BilibiliVideoComment

    client = get_neo4j_client()
    _ensure_platform_node(client, "bilibili", "Bilibili")

    videos = BilibiliVideo.objects.using("mysql").all()
    if limit:
        videos = videos[:limit]

    content_synced = 0
    keywords_synced = 0
    comments_synced = 0

    with client.session() as session:
        for video in videos:
            try:
                content_id = str(video.video_id)
                content_data = {
                    "contentId": content_id,
                    "platform": "bilibili",
                    "contentType": "video",
                    "title": _safe_str(video.title),
                    "author": _safe_str(video.nickname),
                    "authorId": _safe_str(video.user_id),
                    "url": _safe_str(video.video_url),
                    "createTime": _timestamp_to_iso(video.create_time),
                    "likedCount": _safe_int(video.liked_count),
                    "commentCount": _safe_int(video.video_comment),
                }
                _sync_content_node(session, content_data)
                content_synced += 1

                # Extract and sync keywords
                keywords = extract_keywords(
                    video.source_keyword,
                    video.title,
                    video.desc,
                )
                keywords_synced += _sync_keyword_nodes(session, content_id, "bilibili", keywords)

                # Sync comments for this video
                comments = BilibiliVideoComment.objects.using("mysql").filter(video_id=video.video_id)[:50]
                for comment in comments:
                    comment_data = {
                        "commentId": str(comment.comment_id),
                        "platform": "bilibili",
                        "contentId": content_id,
                        "content": _safe_str(comment.content)[:500],
                        "author": _safe_str(comment.nickname),
                        "authorId": _safe_str(comment.user_id),
                        "createTime": _timestamp_to_iso(comment.create_time),
                        "likedCount": _safe_int(comment.like_count),
                    }
                    _sync_comment_node(session, comment_data)
                    comments_synced += 1

            except Exception as e:
                logger.error(f"Error syncing Bilibili video {video.video_id}: {e}")
                continue

    return {
        "content_synced": content_synced,
        "keywords_synced": keywords_synced,
        "comments_synced": comments_synced,
    }


def sync_douyin_content(limit: int | None = None) -> dict[str, int]:
    """Sync Douyin awemes and comments to Neo4j."""
    from apps.media_crawl.models import DouyinAweme, DouyinAwemeComment

    client = get_neo4j_client()
    _ensure_platform_node(client, "douyin", "抖音")

    awemes = DouyinAweme.objects.using("mysql").all()
    if limit:
        awemes = awemes[:limit]

    content_synced = 0
    keywords_synced = 0
    comments_synced = 0

    with client.session() as session:
        for aweme in awemes:
            try:
                content_id = str(aweme.aweme_id)
                content_data = {
                    "contentId": content_id,
                    "platform": "douyin",
                    "contentType": _safe_str(aweme.aweme_type) or "video",
                    "title": _safe_str(aweme.title),
                    "author": _safe_str(aweme.nickname),
                    "authorId": _safe_str(aweme.user_id),
                    "url": _safe_str(aweme.aweme_url),
                    "createTime": _timestamp_to_iso(aweme.create_time),
                    "likedCount": _safe_int(aweme.liked_count),
                    "commentCount": _safe_int(aweme.comment_count),
                }
                _sync_content_node(session, content_data)
                content_synced += 1

                # Extract and sync keywords
                keywords = extract_keywords(
                    aweme.source_keyword,
                    aweme.title,
                    aweme.desc,
                )
                keywords_synced += _sync_keyword_nodes(session, content_id, "douyin", keywords)

                # Sync comments
                comments = DouyinAwemeComment.objects.using("mysql").filter(aweme_id=aweme.aweme_id)[:50]
                for comment in comments:
                    comment_data = {
                        "commentId": str(comment.comment_id),
                        "platform": "douyin",
                        "contentId": content_id,
                        "content": _safe_str(comment.content)[:500],
                        "author": _safe_str(comment.nickname),
                        "authorId": _safe_str(comment.user_id),
                        "createTime": _timestamp_to_iso(comment.create_time),
                        "likedCount": _safe_int(comment.like_count),
                    }
                    _sync_comment_node(session, comment_data)
                    comments_synced += 1

            except Exception as e:
                logger.error(f"Error syncing Douyin aweme {aweme.aweme_id}: {e}")
                continue

    return {
        "content_synced": content_synced,
        "keywords_synced": keywords_synced,
        "comments_synced": comments_synced,
    }


def sync_kuaishou_content(limit: int | None = None) -> dict[str, int]:
    """Sync Kuaishou videos and comments to Neo4j."""
    from apps.media_crawl.models import KuaishouVideo, KuaishouVideoComment

    client = get_neo4j_client()
    _ensure_platform_node(client, "kuaishou", "快手")

    videos = KuaishouVideo.objects.using("mysql").all()
    if limit:
        videos = videos[:limit]

    content_synced = 0
    keywords_synced = 0
    comments_synced = 0

    with client.session() as session:
        for video in videos:
            try:
                content_id = str(video.video_id)
                content_data = {
                    "contentId": content_id,
                    "platform": "kuaishou",
                    "contentType": "video",
                    "title": _safe_str(video.title),
                    "author": _safe_str(video.nickname),
                    "authorId": _safe_str(video.user_id),
                    "url": _safe_str(video.video_url),
                    "createTime": _timestamp_to_iso(video.create_time),
                    "likedCount": _safe_int(video.liked_count),
                    "commentCount": 0,
                }
                _sync_content_node(session, content_data)
                content_synced += 1

                # Extract and sync keywords
                keywords = extract_keywords(
                    video.source_keyword,
                    video.title,
                    video.desc,
                )
                keywords_synced += _sync_keyword_nodes(session, content_id, "kuaishou", keywords)

                # Sync comments
                comments = KuaishouVideoComment.objects.using("mysql").filter(video_id=video.video_id)[:50]
                for comment in comments:
                    comment_data = {
                        "commentId": str(comment.comment_id),
                        "platform": "kuaishou",
                        "contentId": content_id,
                        "content": _safe_str(comment.content)[:500],
                        "author": _safe_str(comment.nickname),
                        "authorId": _safe_str(comment.user_id),
                        "createTime": _timestamp_to_iso(comment.create_time),
                        "likedCount": 0,
                    }
                    _sync_comment_node(session, comment_data)
                    comments_synced += 1

            except Exception as e:
                logger.error(f"Error syncing Kuaishou video {video.video_id}: {e}")
                continue

    return {
        "content_synced": content_synced,
        "keywords_synced": keywords_synced,
        "comments_synced": comments_synced,
    }


def sync_weibo_content(limit: int | None = None) -> dict[str, int]:
    """Sync Weibo notes and comments to Neo4j."""
    from apps.media_crawl.models import WeiboNote, WeiboNoteComment

    client = get_neo4j_client()
    _ensure_platform_node(client, "weibo", "微博")

    notes = WeiboNote.objects.using("mysql").all()
    if limit:
        notes = notes[:limit]

    content_synced = 0
    keywords_synced = 0
    comments_synced = 0

    with client.session() as session:
        for note in notes:
            try:
                content_id = str(note.note_id)
                content_data = {
                    "contentId": content_id,
                    "platform": "weibo",
                    "contentType": "note",
                    "title": _safe_str(note.content)[:100],  # Use content start as title
                    "author": _safe_str(note.nickname),
                    "authorId": _safe_str(note.user_id),
                    "url": _safe_str(note.note_url),
                    "createTime": _timestamp_to_iso(note.create_time),
                    "likedCount": _safe_int(note.liked_count),
                    "commentCount": _safe_int(note.comments_count),
                }
                _sync_content_node(session, content_data)
                content_synced += 1

                # Extract keywords (Weibo uses content as main text)
                keywords = extract_keywords(
                    note.source_keyword,
                    note.content,
                    None,
                )
                keywords_synced += _sync_keyword_nodes(session, content_id, "weibo", keywords)

                # Sync comments
                comments = WeiboNoteComment.objects.using("mysql").filter(note_id=note.note_id)[:50]
                for comment in comments:
                    comment_data = {
                        "commentId": str(comment.comment_id),
                        "platform": "weibo",
                        "contentId": content_id,
                        "content": _safe_str(comment.content)[:500],
                        "author": _safe_str(comment.nickname),
                        "authorId": _safe_str(comment.user_id),
                        "createTime": _timestamp_to_iso(comment.create_time),
                        "likedCount": _safe_int(comment.comment_like_count),
                    }
                    _sync_comment_node(session, comment_data)
                    comments_synced += 1

            except Exception as e:
                logger.error(f"Error syncing Weibo note {note.note_id}: {e}")
                continue

    return {
        "content_synced": content_synced,
        "keywords_synced": keywords_synced,
        "comments_synced": comments_synced,
    }


def sync_tieba_content(limit: int | None = None) -> dict[str, int]:
    """Sync Tieba notes and comments to Neo4j."""
    from apps.media_crawl.models import TiebaNote, TiebaComment

    client = get_neo4j_client()
    _ensure_platform_node(client, "tieba", "贴吧")

    notes = TiebaNote.objects.using("mysql").all()
    if limit:
        notes = notes[:limit]

    content_synced = 0
    keywords_synced = 0
    comments_synced = 0

    with client.session() as session:
        for note in notes:
            try:
                content_id = str(note.note_id)
                content_data = {
                    "contentId": content_id,
                    "platform": "tieba",
                    "contentType": "post",
                    "title": _safe_str(note.title),
                    "author": _safe_str(note.user_nickname),
                    "authorId": "",  # Tieba uses user_link instead
                    "url": _safe_str(note.note_url),
                    "createTime": _safe_str(note.publish_time),
                    "likedCount": 0,
                    "commentCount": _safe_int(note.total_replay_num),
                }
                _sync_content_node(session, content_data)
                content_synced += 1

                # Extract keywords (include tieba_name as keyword)
                keywords = extract_keywords(
                    note.source_keyword,
                    note.title,
                    note.desc,
                )
                if note.tieba_name:
                    keywords.append(note.tieba_name.lower())
                keywords_synced += _sync_keyword_nodes(session, content_id, "tieba", keywords)

                # Sync comments
                comments = TiebaComment.objects.using("mysql").filter(note_id=note.note_id)[:50]
                for comment in comments:
                    comment_data = {
                        "commentId": str(comment.comment_id),
                        "platform": "tieba",
                        "contentId": content_id,
                        "content": _safe_str(comment.content)[:500],
                        "author": _safe_str(comment.user_nickname),
                        "authorId": "",
                        "createTime": _safe_str(comment.publish_time),
                        "likedCount": 0,
                    }
                    _sync_comment_node(session, comment_data)
                    comments_synced += 1

            except Exception as e:
                logger.error(f"Error syncing Tieba note {note.note_id}: {e}")
                continue

    return {
        "content_synced": content_synced,
        "keywords_synced": keywords_synced,
        "comments_synced": comments_synced,
    }


def sync_zhihu_content(limit: int | None = None) -> dict[str, int]:
    """Sync Zhihu content and comments to Neo4j."""
    from apps.media_crawl.models import ZhihuContent, ZhihuComment

    client = get_neo4j_client()
    _ensure_platform_node(client, "zhihu", "知乎")

    contents = ZhihuContent.objects.using("mysql").all()
    if limit:
        contents = contents[:limit]

    content_synced = 0
    keywords_synced = 0
    comments_synced = 0

    with client.session() as session:
        for content in contents:
            try:
                content_id = str(content.content_id)
                content_data = {
                    "contentId": content_id,
                    "platform": "zhihu",
                    "contentType": _safe_str(content.content_type) or "answer",
                    "title": _safe_str(content.title),
                    "author": _safe_str(content.user_nickname),
                    "authorId": _safe_str(content.user_id),
                    "url": _safe_str(content.content_url),
                    "createTime": _safe_str(content.created_time),
                    "likedCount": _safe_int(content.voteup_count),
                    "commentCount": _safe_int(content.comment_count),
                }
                _sync_content_node(session, content_data)
                content_synced += 1

                # Extract keywords
                keywords = extract_keywords(
                    content.source_keyword,
                    content.title,
                    content.desc,
                )
                keywords_synced += _sync_keyword_nodes(session, content_id, "zhihu", keywords)

                # Sync comments
                comments = ZhihuComment.objects.using("mysql").filter(content_id=content.content_id)[:50]
                for comment in comments:
                    comment_data = {
                        "commentId": str(comment.comment_id),
                        "platform": "zhihu",
                        "contentId": content_id,
                        "content": _safe_str(comment.content)[:500],
                        "author": _safe_str(comment.user_nickname),
                        "authorId": _safe_str(comment.user_id),
                        "createTime": _safe_str(comment.publish_time),
                        "likedCount": _safe_int(comment.like_count),
                    }
                    _sync_comment_node(session, comment_data)
                    comments_synced += 1

            except Exception as e:
                logger.error(f"Error syncing Zhihu content {content.content_id}: {e}")
                continue

    return {
        "content_synced": content_synced,
        "keywords_synced": keywords_synced,
        "comments_synced": comments_synced,
    }


# ============================================================================
# Main Sync Functions
# ============================================================================

def sync_xhs_content(limit: int | None = None) -> dict[str, int]:
    """Sync Xiaohongshu (XHS) notes and comments to Neo4j."""
    from apps.media_crawl.models import XhsNote, XhsNoteComment

    client = get_neo4j_client()
    _ensure_platform_node(client, "xhs", "小红书")

    notes = XhsNote.objects.using("mysql").all()
    if limit:
        notes = notes[:limit]

    content_synced = 0
    keywords_synced = 0
    comments_synced = 0

    with client.session() as session:
        for note in notes:
            try:
                content_id = str(note.note_id)
                content_data = {
                    "contentId": content_id,
                    "platform": "xhs",
                    "contentType": _safe_str(note.type) or "note",
                    "title": _safe_str(note.title),
                    "author": _safe_str(note.nickname),
                    "authorId": _safe_str(note.user_id),
                    "url": _safe_str(note.note_url),
                    "createTime": _timestamp_to_iso(note.time),
                    "likedCount": _safe_int(note.liked_count),
                    "commentCount": _safe_int(note.comment_count),
                }
                _sync_content_node(session, content_data)
                content_synced += 1

                # Extract keywords (XHS has tag_list)
                keywords = extract_keywords(
                    note.source_keyword,
                    note.title,
                    note.desc,
                    note.tag_list,
                )
                keywords_synced += _sync_keyword_nodes(session, content_id, "xhs", keywords)

                # Sync comments
                comments = XhsNoteComment.objects.using("mysql").filter(note_id=note.note_id)[:50]
                for comment in comments:
                    comment_data = {
                        "commentId": str(comment.comment_id),
                        "platform": "xhs",
                        "contentId": content_id,
                        "content": _safe_str(comment.content)[:500],
                        "author": _safe_str(comment.nickname),
                        "authorId": _safe_str(comment.user_id),
                        "createTime": _timestamp_to_iso(comment.create_time),
                        "likedCount": _safe_int(comment.like_count),
                    }
                    _sync_comment_node(session, comment_data)
                    comments_synced += 1

            except Exception as e:
                logger.error(f"Error syncing XHS note {note.note_id}: {e}")
                continue

    return {
        "content_synced": content_synced,
        "keywords_synced": keywords_synced,
        "comments_synced": comments_synced,
    }


PLATFORM_SYNC_FUNCTIONS = {
    "bilibili": sync_bilibili_content,
    "douyin": sync_douyin_content,
    "kuaishou": sync_kuaishou_content,
    "weibo": sync_weibo_content,
    "xhs": sync_xhs_content,
    "tieba": sync_tieba_content,
    "zhihu": sync_zhihu_content,
}


def sync_platform_content(
    platform: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """
    Sync media content to Neo4j.

    Args:
        platform: Platform name (bilibili, douyin, etc.) or None for all platforms
        limit: Maximum content items per platform

    Returns:
        Summary of sync operation

    Future: This function can be called automatically after crawl completes.
    """
    results: dict[str, Any] = {
        "platforms": {},
        "totals": {
            "content_synced": 0,
            "keywords_synced": 0,
            "comments_synced": 0,
        },
    }

    platforms_to_sync = [platform] if platform else SUPPORTED_PLATFORMS

    for p in platforms_to_sync:
        if p not in PLATFORM_SYNC_FUNCTIONS:
            logger.warning(f"Unknown platform: {p}")
            continue

        logger.info(f"Starting Neo4j sync for platform: {p}")
        try:
            sync_func = PLATFORM_SYNC_FUNCTIONS[p]
            platform_result = sync_func(limit=limit)
            results["platforms"][p] = platform_result

            for key in ["content_synced", "keywords_synced", "comments_synced"]:
                results["totals"][key] += platform_result.get(key, 0)

            logger.info(f"Completed Neo4j sync for {p}: {platform_result}")
        except Exception as e:
            logger.error(f"Error syncing platform {p}: {e}")
            results["platforms"][p] = {"error": str(e)}

    return results


def update_sync_status(
    status: str,
    progress: int = 0,
    last_result: dict[str, Any] | None = None,
) -> None:
    """Update sync status in cache."""
    cache.set(
        SYNC_STATUS_CACHE_KEY,
        {
            "status": status,
            "progress": progress,
            "lastSyncTime": datetime.now().isoformat() if status == "idle" else None,
            "lastResult": last_result,
            "updatedAt": datetime.now().isoformat(),
        },
        timeout=3600,  # 1 hour
    )


def get_sync_status() -> dict[str, Any]:
    """Get current sync status from cache."""
    status = cache.get(SYNC_STATUS_CACHE_KEY)
    if status is None:
        return {
            "status": "idle",
            "progress": 0,
            "lastSyncTime": None,
            "lastResult": None,
        }
    return status


# ============================================================================
# Graph Data Retrieval
# ============================================================================

def get_media_graph_data(
    platform: str | None = None,
    keyword: str | None = None,
    limit: int = 100,
) -> dict[str, Any]:
    """
    Fetch media graph data from Neo4j.

    Args:
        platform: Filter by platform name
        keyword: Filter by keyword
        limit: Maximum nodes to return

    Returns:
        Graph data with nodes and edges
    """
    client = get_neo4j_client()

    # Select appropriate query based on filters
    query_name = "ALL_PLATFORMS"
    if platform and keyword:
        query = GET_MEDIA_GRAPH_BY_PLATFORM_AND_KEYWORD_QUERY
        params = {"platform": platform, "keyword": keyword, "limit": limit}
        query_name = "BY_PLATFORM_AND_KEYWORD"
    elif keyword:
        query = GET_MEDIA_GRAPH_BY_KEYWORD_QUERY
        params = {"keyword": keyword, "limit": limit}
        query_name = "BY_KEYWORD"
    elif platform:
        query = GET_MEDIA_GRAPH_BY_PLATFORM_QUERY
        params = {"platform": platform, "limit": limit}
        query_name = "BY_PLATFORM"
    else:
        query = GET_MEDIA_GRAPH_ALL_PLATFORMS_QUERY
        params = {"limit": limit}

    logger.info(f"get_media_graph_data using query: {query_name}, params: {params}")

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    node_ids: set[str] = set()

    with client.session() as session:
        result = session.run(query, params)
        records = list(result)  # Consume result to count
        logger.info(f"get_media_graph_data query returned {len(records)} records")

        for record in records:
            platform_node = record.get("p")
            content_node = record.get("c")
            keywords_list = record.get("keywords", [])
            comment_count = record.get("commentCount", 0)

            # Add platform node
            if platform_node:
                platform_id = f"platform_{platform_node.get('name')}"
                if platform_id not in node_ids:
                    nodes.append({
                        "id": platform_id,
                        "type": "Platform",
                        "label": platform_node.get("displayName", platform_node.get("name")),
                        "properties": _serialize_node_properties(platform_node),
                    })
                    node_ids.add(platform_id)

            # Add content node
            if content_node:
                content_id = f"content_{content_node.get('platform')}_{content_node.get('contentId')}"
                if content_id not in node_ids:
                    content_props = _serialize_node_properties(content_node)
                    content_props["commentCount"] = comment_count
                    nodes.append({
                        "id": content_id,
                        "type": "Content",
                        "label": (content_node.get("title") or "")[:50],
                        "properties": content_props,
                    })
                    node_ids.add(content_id)

                    # Add HAS_CONTENT edge
                    if platform_node:
                        platform_id = f"platform_{platform_node.get('name')}"
                        edges.append({
                            "source": platform_id,
                            "target": content_id,
                            "type": "HAS_CONTENT",
                        })

                # Add keyword nodes and edges
                for kw in keywords_list:
                    if kw:
                        kw_name = kw.get("name", "")
                        kw_id = f"keyword_{kw_name}"
                        if kw_id not in node_ids:
                            nodes.append({
                                "id": kw_id,
                                "type": "Keyword",
                                "label": kw_name,
                                "properties": _serialize_node_properties(kw),
                            })
                            node_ids.add(kw_id)

                        edges.append({
                            "source": content_id,
                            "target": kw_id,
                            "type": "HAS_KEYWORD",
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


def get_media_keywords(
    platform: str | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """
    Get popular keywords for media content.

    Args:
        platform: Filter by platform name
        limit: Maximum keywords to return

    Returns:
        List of keywords with counts
    """
    client = get_neo4j_client()

    # Use appropriate query based on whether platform filter is provided
    if platform:
        query = GET_POPULAR_KEYWORDS_BY_PLATFORM_QUERY
        params = {"platform": platform, "limit": limit}
    else:
        query = GET_POPULAR_KEYWORDS_ALL_QUERY
        params = {"limit": limit}

    results = client.run_query(query, params)
    return [{"name": r["name"], "count": r["count"]} for r in results]


def search_media_keywords(query_text: str, limit: int = 20) -> list[dict[str, Any]]:
    """
    Search keywords by text matching.

    Args:
        query_text: Search query
        limit: Maximum results to return

    Returns:
        List of matching keywords with counts
    """
    if not query_text or len(query_text) < 2:
        return []

    client = get_neo4j_client()
    results = client.run_query(
        SEARCH_KEYWORDS_QUERY,
        {"query": query_text, "limit": limit},
    )
    return [{"name": r["name"], "count": r["count"]} for r in results]

