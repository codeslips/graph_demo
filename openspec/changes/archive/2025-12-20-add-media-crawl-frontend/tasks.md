# Tasks: Add Media Crawl Frontend Management Page

## 1. Setup & Types
- [x] 1.1 Create `frontend/src/types/media.ts` with TypeScript interfaces for all platform models
- [x] 1.2 Create `frontend/src/api/media.ts` with API functions for all CRUD operations

## 2. State Management
- [x] 2.1 Create `frontend/src/stores/media.ts` Pinia store for media data state

## 3. Components
- [x] 3.1 Create `frontend/src/components/media/PlatformTabs.vue` - Platform tab navigation
- [x] 3.2 Create `frontend/src/components/media/MediaDataTable.vue` - Data table with pagination
- [x] 3.3 Create `frontend/src/components/media/MediaFilters.vue` - Filter controls
- [x] 3.4 Create `frontend/src/components/media/MediaFormModal.vue` - Create/Edit modal
- [x] 3.5 Create `frontend/src/components/media/DeleteConfirmModal.vue` - Delete confirmation

## 4. Views & Routes
- [x] 4.1 Create `frontend/src/views/MediaView.vue` - Main media management page
- [x] 4.2 Create `frontend/src/views/MediaDetailView.vue` - Detail view for single record
- [x] 4.3 Update `frontend/src/router/index.ts` - Add media routes

## 5. Navigation Integration
- [x] 5.1 Update `frontend/src/App.vue` - Add "媒体数据" navigation link
