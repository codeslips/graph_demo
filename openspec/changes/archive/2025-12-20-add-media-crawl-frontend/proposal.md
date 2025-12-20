# Change: Add Media Crawl Frontend Management Page

## Why
The backend `media_crawl` API provides CRUD endpoints for 7 social media platforms (Bilibili, Douyin, Kuaishou, Weibo, XHS, Tieba, Zhihu), but there is no frontend interface to manage this data. Users need a unified management page to view, create, edit, and delete media crawl records.

## What Changes
- Add new "媒体数据" navigation button to the main app navigation
- Create unified media management view with platform tabs
- Implement data table component with pagination and filtering
- Add create/edit modal forms for each platform entity type
- Implement single and batch delete functionality
- Create API layer for media crawl endpoints
- Add TypeScript types for all platform models
- Add Pinia store for media data state management

## Impact
- Affected specs: `media-crawl-frontend` (new capability)
- Affected code:
  - `frontend/src/App.vue` - Add navigation link
  - `frontend/src/router/index.ts` - Add new routes
  - `frontend/src/views/` - New MediaView.vue and related views
  - `frontend/src/components/media/` - New media components
  - `frontend/src/api/media.ts` - New API functions
  - `frontend/src/types/media.ts` - New type definitions
  - `frontend/src/stores/media.ts` - New Pinia store

