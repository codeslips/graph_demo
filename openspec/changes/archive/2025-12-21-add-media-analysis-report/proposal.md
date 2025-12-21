# Change: Add Media Analysis Report Feature

## Why

Users need to generate AI-powered analysis reports from media crawl data. This allows them to get insights about travel trends, user demographics, popular destinations, and content patterns from social media data (XHS, Douyin, Weibo, etc.). Reports should be saveable and viewable with markdown rendering.

## What Changes

- Add "生成分析报告" (Generate Analysis Report) button to MediaView.vue
- Add dialog for selecting source_keyword (with validation) and time range filter
- Create new API endpoint to fetch unique source_keywords from database
- Create new API endpoint to export filtered data in CSV-like format
- Integrate with existing Coze API to generate AI analysis report
- Add new Django model `AnalysisReport` to persist reports
- Add CRUD API endpoints for reports (create, list, get, delete)
- Add new navigation link "报告列表" for saved reports
- Create new ReportListView and ReportDetailView pages with markdown rendering
- Add "保存报告" button to save generated reports

## Impact

- Affected specs: 
  - NEW: `media-analysis-report-api` - Backend API for reports
  - NEW: `media-analysis-report-frontend` - Frontend UI for reports
  - MODIFIED: `media-crawl-frontend` - Add "生成分析报告" button to MediaView
- Affected code:
  - `backend/apps/media_crawl/models/` - New `AnalysisReport` model
  - `backend/apps/media_crawl/api/` - New report API endpoints
  - `frontend/src/views/MediaView.vue` - Add report generation button and dialog
  - `frontend/src/views/` - New `ReportListView.vue`, `ReportDetailView.vue`
  - `frontend/src/components/media/` - New `ReportGeneratorModal.vue`
  - `frontend/src/router/index.ts` - New routes for reports
  - `frontend/src/api/` - New report API functions

