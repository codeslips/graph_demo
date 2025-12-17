# Tasks: ThePaper Crawl System Implementation

## 1. Backend - Crawl Models and Migrations

- [x] 1.1 Implement `CrawlTask` model with status enum (PENDING, RUNNING, DONE, FAILED)
- [x] 1.2 Implement `CrawlItem` model with foreign key to CrawlTask
- [x] 1.3 Create and run database migrations
- [x] 1.4 Register models in Django admin

## 2. Backend - ThePaper Crawler Integration

- [x] 2.1 Create `crawler/thepaper/config.py` with API URLs and headers
- [x] 2.2 Create `crawler/thepaper/news_list.py` for channel list fetching
- [x] 2.3 Create `crawler/thepaper/article.py` for article detail parsing
- [x] 2.4 Create `crawler/utils/http_client.py` with async httpx wrapper

## 3. Backend - Celery Tasks

- [x] 3.1 Add `tasks.py` to crawl app with `execute_crawl_task`
- [x] 3.2 Implement task status update logic
- [x] 3.3 Add error handling and retry logic

## 4. Backend - Neo4j Sync Service

- [x] 4.1 Implement `Neo4jClient` with connection management
- [x] 4.2 Create `neo4j_sync.py` with node/relationship creation
- [x] 4.3 Implement batch sync after crawl completion
- [x] 4.4 Add `neo4j_synced` flag update logic

## 5. Backend - Crawl API Endpoints

- [x] 5.1 Create `apps/crawl/schemas.py` with request/response schemas
- [x] 5.2 Create `apps/crawl/api.py` with Django Ninja router
- [x] 5.3 Implement POST `/api/v1/crawl/tasks` (create task)
- [x] 5.4 Implement GET `/api/v1/crawl/tasks` (list tasks)
- [x] 5.5 Implement GET `/api/v1/crawl/tasks/{id}` (task detail)
- [x] 5.6 Implement DELETE `/api/v1/crawl/tasks/{id}` (cancel/delete)
- [x] 5.7 Register crawl API router in main urls.py

## 6. Backend - Graph API Endpoints

- [x] 6.1 Create `apps/graph/schemas.py` with graph data schemas
- [x] 6.2 Create `apps/graph/api.py` with Django Ninja router
- [x] 6.3 Implement GET `/api/v1/graph/task/{id}` (task graph data)
- [x] 6.4 Implement GET `/api/v1/graph/keywords` (popular tags)
- [x] 6.5 Implement GET `/api/v1/graph/search` (node search)
- [x] 6.6 Register graph API router in main urls.py

## 7. Frontend - API Client

- [x] 7.1 Create `api/crawl.ts` with task API functions
- [x] 7.2 Create `api/graph.ts` with graph API functions
- [x] 7.3 Define TypeScript types in `types/crawl.ts` and `types/graph.ts`

## 8. Frontend - Pinia Stores

- [x] 8.1 Create `stores/task.ts` for task state management
- [x] 8.2 Create `stores/graph.ts` for graph state management

## 9. Frontend - Task Management UI

- [x] 9.1 Create `components/task/TaskForm.vue` for creating crawl tasks
- [x] 9.2 Create `components/task/TaskCard.vue` for task display
- [x] 9.3 Create `components/task/TaskProgress.vue` for progress indicator
- [x] 9.4 Implement `views/TaskListView.vue` with form and task list
- [x] 9.5 Implement `views/TaskDetailView.vue` with task info and items

## 10. Frontend - Graph Visualization

- [x] 10.1 Install ECharts: `pnpm add echarts`
- [x] 10.2 Create `components/graph/GraphCanvas.vue` with ECharts integration
- [x] 10.3 Create `components/graph/NodeDetail.vue` for node info panel
- [x] 10.4 Create `components/graph/GraphLegend.vue` for node type legend
- [x] 10.5 Implement `views/GraphView.vue` with full graph UI
- [x] 10.6 Add polling for real-time task status in composables

## 11. Frontend - Styling and Polish

- [x] 11.1 Style task form with proper inputs and validation
- [x] 11.2 Style graph canvas with proper sizing and controls
- [x] 11.3 Add loading states and error handling UI
