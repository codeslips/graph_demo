# Design: ThePaper Crawl System

## Context

The project skeleton exists with Docker infrastructure, but all business logic is placeholder. A working crawler prototype exists in `scripts/crawl_thepaper.py` that demonstrates:
- Fetching channel content via ThePaper's API (`api.thepaper.cn`)
- Parsing article detail pages via mobile site (`m.thepaper.cn`)
- Extracting structured data including tags, channel info, authors

This design integrates the prototype into the full stack.

## Goals / Non-Goals

### Goals
- Async crawl execution via Celery (no blocking HTTP requests)
- Reliable data persistence in PostgreSQL with Neo4j sync
- Interactive graph visualization showing article-tag-channel relationships
- Simple task management UI for starting and monitoring crawls

### Non-Goals
- Advanced NLP/keyword extraction (use existing tags from articles)
- Real-time WebSocket updates (polling is sufficient for MVP)
- User authentication (public access for demo)
- Scheduled/recurring crawls (manual trigger only)

## Decisions

### 1. Data Flow Architecture

```
User → Vue Form → Django API → Create CrawlTask (PostgreSQL)
                            → Dispatch Celery Task
                            
Celery Worker → Fetch Channel List (ThePaper API)
              → Parse Each Article Detail
              → Save CrawlItems (PostgreSQL)
              → Sync to Neo4j (Nodes + Relationships)
              → Update Task Status
              
User → Vue Graph → Django Graph API → Query Neo4j
                                     → Return nodes/edges JSON
                                     → Render ECharts
```

**Rationale**: This follows the architecture defined in `project.md` and keeps concerns separated.

### 2. Graph Schema

Based on the crawled data structure from `32169777.json`:

```cypher
// Core Nodes
(:Website {domain: "thepaper.cn", name: "澎湃新闻"})
(:Channel {nodeId: int, name: str, desc: str})
(:Article {contId: str, title: str, author: str, pubTime: datetime, url: str, summary: str})
(:Tag {tagId: int, name: str})

// Relationships
(:Website)-[:HAS_CHANNEL]->(:Channel)
(:Channel)-[:CONTAINS]->(:Article)
(:Article)-[:HAS_TAG]->(:Tag)
```

**Rationale**: 
- `Website` is singleton for ThePaper, enables future multi-source support
- Tags are first-class nodes to enable tag-based exploration
- Authors embedded as Article property (not separate node) for simplicity

### 3. Celery Task Design

Single main task that orchestrates the crawl:

```python
@shared_task(bind=True, max_retries=3)
def execute_crawl_task(self, task_id: str):
    # 1. Mark RUNNING
    # 2. Fetch list from channel API
    # 3. For each article: fetch detail, save CrawlItem
    # 4. Batch sync to Neo4j
    # 5. Mark DONE or FAILED
```

**Rationale**: Single task simplifies error handling and status tracking. Batch Neo4j sync is more efficient than per-item sync.

### 4. Frontend Graph Library

**Decision**: Use ECharts with `graph` series type

**Alternatives considered**:
- Cytoscape.js: More powerful but heavier, overkill for this use case
- D3.js: Low-level, requires more code
- vis.js: Good but less maintained

**Rationale**: ECharts is already commonly used in Vue projects, has excellent force-layout support, and provides good defaults for interactive graphs.

### 5. API Response Format for Graph

```json
{
  "nodes": [
    {"id": "article_32169777", "type": "Article", "label": "吉利20亿...", "properties": {...}},
    {"id": "tag_307653", "type": "Tag", "label": "吉利汽车", "properties": {...}},
    {"id": "channel_26490", "type": "Channel", "label": "汽车圈", "properties": {...}}
  ],
  "edges": [
    {"source": "channel_26490", "target": "article_32169777", "type": "CONTAINS"},
    {"source": "article_32169777", "target": "tag_307653", "type": "HAS_TAG"}
  ],
  "stats": {
    "totalNodes": 150,
    "totalEdges": 420,
    "nodesByType": {"Article": 100, "Tag": 45, "Channel": 5}
  }
}
```

**Rationale**: Flat structure is easy to transform to ECharts format, includes stats for UI display.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| ThePaper API changes | Selectors in config file, easy to update |
| Rate limiting | Configurable delay between requests (default 0.5s) |
| Neo4j sync failures | `neo4j_synced` flag enables retry of failed items |
| Large graphs slow to render | Pagination in API, limit nodes returned |

## Migration Plan

Not applicable - this is new functionality, no existing data to migrate.

## Open Questions

None - the crawler prototype has validated the data extraction approach.

