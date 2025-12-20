# Change: Add Media Data Neo4j Sync and Graph Visualization

## Why

The system currently only syncs ThePaper crawl data to Neo4j for graph visualization. Media platform data (Bilibili, Douyin, Kuaishou, Weibo, Tieba, Zhihu) stored in MySQL has no graph representation, limiting relationship analysis and visualization capabilities for social media content.

## What Changes

### Backend
- Add Celery task `sync_media_to_neo4j` for syncing media data from MySQL to Neo4j
- Create Neo4j graph model for media data: `Platform → Content → Keywords/Tags + Comments`
- Add API endpoints for media graph data and keyword search
- Add manual sync trigger endpoint
- Support 7 platforms: Bilibili, Douyin, Kuaishou, Weibo, XHS, Tieba, Zhihu

### Frontend
- Add new `/media-graph` route for media graph visualization
- Reuse existing `GraphCanvas`, `NodeDetail`, `GraphLegend` components
- Add platform/keyword filtering for different graph views
- Add "Sync to Neo4j" button on media page

### Infrastructure
- Design sync mechanism to support future automatic sync after media crawl updates

## Impact

- Affected specs: `neo4j-sync` (modified), `media-crawl-api` (modified)
- New specs: `media-neo4j-sync`, `media-graph-frontend`
- Affected code:
  - `backend/services/neo4j_sync.py` (extend with media sync)
  - `backend/apps/media_crawl/api/` (add sync trigger endpoint)
  - `backend/apps/graph/api.py` (add media graph endpoints)
  - `frontend/src/views/MediaGraphView.vue` (new)
  - `frontend/src/stores/mediaGraph.ts` (new)
  - `frontend/src/api/mediaGraph.ts` (new)

