# Change: Implement ThePaper Crawl System with Neo4j Graph Storage and Visualization

## Why

The project has a working prototype crawler (`scripts/crawl_thepaper.py`) that can fetch news from 澎湃新闻 (ThePaper), but lacks the full system integration needed to:
1. Execute crawls asynchronously via Celery
2. Store crawled data in PostgreSQL and sync to Neo4j as a graph
3. Expose graph data via API for frontend visualization
4. Display interactive graph visualizations in the Vue frontend

This change implements the complete data pipeline from crawling to visualization.

## What Changes

### Backend - Crawl Tasks Capability
- Implement `CrawlTask` and `CrawlItem` Django models
- Add Celery tasks for async crawl execution
- Create Django Ninja API endpoints for task CRUD operations
- Integrate existing crawler logic from `scripts/crawl_thepaper.py`

### Backend - Neo4j Sync Capability
- Implement Neo4j client with connection pooling
- Create sync service to write nodes/relationships after crawl
- Define graph schema (Website, Channel, Article, Tag nodes)

### Backend - Graph API Capability
- Add graph query endpoints for task visualization
- Implement keyword aggregation queries
- Add node search functionality

### Frontend - Graph Visualization Capability
- Implement ECharts force-directed graph component
- Add node detail panel and filtering controls
- Create task management UI with crawl form and progress display

## Impact

- **Affected specs**: Creates 4 new capabilities
  - `crawl-tasks` - Task models and API
  - `neo4j-sync` - Graph database sync
  - `graph-api` - Graph query endpoints
  - `graph-visualization` - Frontend graph display
- **Affected code**:
  - `backend/apps/crawl/` - Models, API, tasks
  - `backend/apps/graph/` - Graph API
  - `backend/services/` - Neo4j client, sync service
  - `backend/crawler/thepaper/` - Crawler implementation
  - `frontend/src/views/` - Task and Graph views
  - `frontend/src/components/` - Task and Graph components
  - `frontend/src/api/` - API client functions
  - `frontend/src/stores/` - Pinia stores

