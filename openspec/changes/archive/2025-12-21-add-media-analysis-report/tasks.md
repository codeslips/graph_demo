## 1. Backend - Model and Migration

- [x] 1.1 Create `AnalysisReport` model in `backend/apps/media_crawl/models/report.py`
- [x] 1.2 Export model in `models/__init__.py`
- [x] 1.3 Register in admin if needed
- [x] 1.4 Create and run migration

## 2. Backend - API Endpoints

- [x] 2.1 Create `report.py` in `backend/apps/media_crawl/api/` with:
  - GET `/source-keywords/` - List unique source_keywords by platform
  - POST `/export-data/` - Export filtered data as CSV-like text
  - POST `/` - Create report
  - GET `/` - List reports (with pagination)
  - GET `/{id}/` - Get report detail
  - DELETE `/{id}/` - Delete report
- [x] 2.2 Create schemas in `backend/apps/media_crawl/schemas/report.py`
- [x] 2.3 Mount router in main API configuration

## 3. Frontend - API Layer

- [x] 3.1 Create `frontend/src/api/report.ts` with functions:
  - `getSourceKeywords(platform)`
  - `exportMediaData(platform, sourceKeyword, timeFrom, timeTo)`
  - `createReport(data)`
  - `getReports(page, limit)`
  - `getReport(id)`
  - `deleteReport(id)`
- [x] 3.2 Create `frontend/src/types/report.ts` with TypeScript interfaces

## 4. Frontend - Report Generator Modal

- [x] 4.1 Create `frontend/src/components/media/ReportGeneratorModal.vue`
  - Source keyword input with validation
  - Time range picker (from/to)
  - Generate button
  - Loading state during generation
  - Report preview area with markdown rendering
  - Save report button

## 5. Frontend - MediaView Integration

- [x] 5.1 Add "生成分析报告" button to `MediaView.vue` header actions
- [x] 5.2 Import and integrate `ReportGeneratorModal` component
- [x] 5.3 Handle modal open/close and report generation flow

## 6. Frontend - Report List View

- [x] 6.1 Create `frontend/src/views/ReportListView.vue`
  - List of saved reports with pagination
  - Report title, platform, source_keyword, created_at
  - Delete button with confirmation
  - Click to view detail
- [x] 6.2 Add route `/reports` to router

## 7. Frontend - Report Detail View

- [x] 7.1 Create `frontend/src/views/ReportDetailView.vue`
  - Display report metadata (title, platform, time range, etc.)
  - Render report content as HTML from markdown
  - Back button to report list
- [x] 7.2 Add route `/reports/:id` to router
- [x] 7.3 Install and configure `marked` + `DOMPurify` for markdown rendering

## 8. Frontend - Navigation

- [x] 8.1 Add "报告列表" navigation link to sidebar/header
