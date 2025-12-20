# Design: Media Data Neo4j Sync and Graph Visualization

## Context

The current system syncs ThePaper news articles to Neo4j using a task-based model (CrawlTask → CrawlItem → Neo4j sync). Media data from social platforms is stored in a separate MySQL database without graph representation.

This change adds Neo4j sync for media data with a content-centric graph model, enabling relationship visualization for social media content.

**Stakeholders:** Users who need to analyze relationships in social media data

## Goals / Non-Goals

### Goals
- Sync media content (videos, notes, posts) and comments to Neo4j
- Extract and link keywords/tags from content descriptions
- Provide graph visualization for media data with keyword-based exploration
- Design for future automatic sync after crawl updates

### Non-Goals
- User relationship graphs (follows, fans) - may be added later
- Full-text search within Neo4j
- Real-time sync during crawl

## Decisions

### Decision 1: Content-Centric Graph Model

**What:** Use `Platform → Content → Keywords + Comments` model

```
(:Platform {name: "Bilibili"})
  -[:HAS_CONTENT]->
(:Content {id, type, platform, title, author, url, ...})
  -[:HAS_KEYWORD {weight}]->
(:Keyword {name})

(:Content)
  -[:HAS_COMMENT]->
(:Comment {id, content, author, ...})
```

**Why:** 
- Simpler than user-centric model
- Keywords enable cross-platform analysis
- Comments show engagement patterns
- Extensible to add user nodes later

**Alternatives considered:**
- User-centric model: More complex, requires user deduplication across platforms
- Flat content model: Loses relationship value

### Decision 2: Unified Content Node with Type Field

**What:** Single `Content` label with `platform` and `contentType` fields instead of separate labels per platform.

**Why:**
- Enables cross-platform queries
- Simplifies Cypher queries
- Consistent API response format

### Decision 3: Manual Sync with Future Hook Support

**What:** Initial implementation uses manual "Sync to Neo4j" button. Service layer designed with entry points for future automatic sync.

**Why:**
- User controls when sync happens
- Lower complexity for initial release
- Clear function signatures for future integration

**Future integration point:**
```python
# services/media_neo4j_sync.py
def sync_platform_content(platform: str, content_ids: list[int] = None) -> dict:
    """
    Sync content to Neo4j. If content_ids is None, syncs all unsynced content.
    Future: Called automatically after crawl completes.
    """
```

### Decision 4: Keyword Extraction Strategy

**What:** Extract keywords from:
- `source_keyword` field (if present)
- Hashtags in `title`/`desc` fields (pattern: `#keyword#` or `#keyword `)
- Tag lists where available (Weibo, XHS models have `tag_list`)

**Why:** Maximizes keyword coverage without requiring NLP dependencies.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Large dataset sync may be slow | Batch processing with progress tracking; optional limit parameter |
| MySQL → Neo4j connectivity | Use same Redis queue as ThePaper sync; robust error handling |
| Keyword extraction inaccuracy | Start with simple patterns; can enhance later |
| Neo4j schema conflicts | Use unique constraints with `platform_contentId` composite key |

## Migration Plan

1. Add Neo4j node/relationship creation without modifying existing data
2. Implement sync service with idempotent operations (MERGE not CREATE)
3. Add API endpoints
4. Add frontend components
5. Test with Bilibili data first, then enable other platforms

**Rollback:** Neo4j data can be deleted by platform label without affecting PostgreSQL/MySQL data.

## Open Questions

- [ ] Should keywords be normalized (lowercase, trimmed)?
- [ ] Maximum sync batch size for performance?
- [ ] Should we track `neo4j_synced` flag on media models (requires MySQL schema change)?

