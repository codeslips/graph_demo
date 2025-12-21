# Change: Add Media Crawl Task Integration

## Why

The project needs to integrate with an external media crawl service to trigger crawl tasks for social media platforms. Currently, the media crawl module only manages data that's already in the database but cannot initiate new crawls. Users need the ability to start crawl tasks from the frontend, monitor their progress, and be notified when complete.

## What Changes

- Add `MEDIA_CRAWL_SERVICE_URL` environment variable configuration
- Create backend API endpoints to proxy to the external media crawl service:
  - `POST /api/v1/media/crawler/start` - Start a new crawl task
  - `GET /api/v1/media/crawler/status` - Get current crawl task status
- Add new frontend page `/media/crawl` for managing crawl tasks
- Implement single-task constraint: prevent creating new tasks while one is running
- Provide form inputs for all crawl parameters (platform, login_type, crawler_type, keywords, etc.)
- Implement status polling to monitor task progress and notify on completion

## Impact

- Affected specs: Creates two new specs (media-crawl-task-api, media-crawl-task-frontend)
- Affected code:
  - `backend/config/settings/base.py` - Add MEDIA_CRAWL_SERVICE_URL env var
  - `backend/apps/media_crawl/api/__init__.py` - Add crawler proxy endpoints
  - `backend/apps/media_crawl/schemas.py` - Add request/response schemas
  - `frontend/src/views/MediaCrawlTaskView.vue` - New page
  - `frontend/src/api/mediaCrawler.ts` - API functions
  - `frontend/src/stores/mediaCrawler.ts` - State management
  - `frontend/src/router/index.ts` - Add route
  - `frontend/src/types/mediaCrawler.ts` - Type definitions

