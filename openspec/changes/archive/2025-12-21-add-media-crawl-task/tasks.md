## 1. Backend Implementation

- [x] 1.1 Add `MEDIA_CRAWL_SERVICE_URL` environment variable to `backend/config/settings/base.py`
- [x] 1.2 Create crawler request/response schemas in `backend/apps/media_crawl/schemas.py`
- [x] 1.3 Add crawler proxy endpoints to `backend/apps/media_crawl/api/__init__.py`:
  - `POST /crawler/start` - Proxy start request to external service
  - `GET /crawler/status` - Proxy status request to external service
- [x] 1.4 Add httpx dependency for async HTTP requests to external service (already in requirements)

## 2. Frontend Implementation

- [x] 2.1 Create TypeScript types in `frontend/src/types/mediaCrawler.ts`
- [x] 2.2 Create API functions in `frontend/src/api/mediaCrawler.ts`
- [x] 2.3 Create Pinia store in `frontend/src/stores/mediaCrawler.ts`
- [x] 2.4 Create MediaCrawlTaskView page in `frontend/src/views/MediaCrawlTaskView.vue`
- [x] 2.5 Add route `/media/crawl` to `frontend/src/router/index.ts`
- [x] 2.6 Add navigation link to MediaView (added "爬虫任务" button)

## 3. Integration

- [x] 3.1 Update `.env.example` with `MEDIA_CRAWL_SERVICE_URL` documentation (file blocked by gitignore, env var documented in base.py with default value)
