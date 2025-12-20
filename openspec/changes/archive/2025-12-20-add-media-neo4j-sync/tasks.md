# Tasks: Add Media Data Neo4j Sync and Graph Visualization

## 1. Backend - Neo4j Sync Service

- [x] 1.1 Create `backend/services/media_neo4j_sync.py` with Cypher queries for media graph model
- [x] 1.2 Implement `sync_platform_content()` function for each platform (Bilibili, Douyin, Kuaishou, Weibo, XHS, Tieba, Zhihu)
- [x] 1.3 Implement keyword extraction from `source_keyword`, hashtags, and tag fields
- [x] 1.4 Add `sync_media_to_neo4j` Celery task in `backend/apps/media_crawl/tasks.py`
- [x] 1.5 Implement `get_media_graph_data()` function for fetching graph by platform/keyword

## 2. Backend - API Endpoints

- [x] 2.1 Add sync trigger endpoint: `POST /api/v1/media/sync-neo4j`
- [x] 2.2 Add media graph data endpoint: `GET /api/v1/graph/media`
- [x] 2.3 Add media keywords endpoint: `GET /api/v1/graph/media/keywords`
- [x] 2.4 Add media graph search endpoint: `GET /api/v1/graph/media/search`
- [x] 2.5 Add sync status endpoint: `GET /api/v1/media/sync-status`

## 3. Frontend - API and Store

- [x] 3.1 Create `frontend/src/api/mediaGraph.ts` with API functions
- [x] 3.2 Create `frontend/src/stores/mediaGraph.ts` Pinia store
- [x] 3.3 Add TypeScript types in `frontend/src/types/mediaGraph.ts`

## 4. Frontend - Graph View

- [x] 4.1 Create `frontend/src/views/MediaGraphView.vue` page component
- [x] 4.2 Add platform filter tabs component
- [x] 4.3 Add keyword search and tag cloud component
- [x] 4.4 Integrate existing `GraphCanvas`, `NodeDetail`, `GraphLegend` components
- [x] 4.5 Add route `/media-graph` to router

## 5. Frontend - Sync Trigger

- [x] 5.1 Add "Sync to Neo4j" button on MediaView.vue
- [x] 5.2 Show sync progress/status indicator
- [x] 5.3 Add sync completion notification

## 6. Integration

- [x] 6.1 Register new API routers in Django config
- [x] 6.2 Add navigation link to media graph in sidebar
