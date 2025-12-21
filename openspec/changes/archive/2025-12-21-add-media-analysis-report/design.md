## Context

Users want to analyze media crawl data and generate AI-powered reports. The system already has:
- Media crawl models with data from 7 platforms (XHS, Douyin, Weibo, etc.)
- Coze chat API integration for AI responses
- Existing MediaView.vue for managing media data

## Goals / Non-Goals

**Goals:**
- Allow users to select source_keyword and time range to filter data
- Export filtered data in CSV-like format for AI analysis
- Generate reports using existing Coze API
- Save and view reports with markdown rendering
- Simple, focused implementation

**Non-Goals:**
- Real-time report generation progress (use simple loading state)
- Report sharing or export to PDF
- Report editing after save
- Multi-platform data aggregation in single report (per-platform only)

## Decisions

### 1. Report Model Design
- **Decision**: Create `AnalysisReport` model in `media_crawl` app
- **Rationale**: Reports are directly tied to media crawl data; keeping them together maintains cohesion
- **Fields**: `id`, `title`, `platform`, `source_keyword`, `time_from`, `time_to`, `content` (markdown), `created_at`

### 2. Data Export Format
- **Decision**: Export data as CSV-like text matching existing model fields
- **Rationale**: User specified "just csv like data" - simple and Coze can parse it
- **Format**: Header row + data rows with fields from the platform's content model
- Example for XHS: `note_id,title,desc,liked_count,collected_count,comment_count,share_count,time,user_id,nickname,ip_location,tag_list`

### 3. Source Keyword Validation
- **Decision**: User inputs keyword, frontend validates against list fetched from API
- **Rationale**: Provides flexibility while ensuring data exists
- **UX**: Input with autocomplete/suggestions, show error if keyword not found

### 4. Markdown Rendering
- **Decision**: Use `marked` library for markdown-to-HTML conversion
- **Rationale**: Lightweight, well-maintained, already common in Vue projects
- **Security**: Sanitize HTML output to prevent XSS

### 5. API Structure
- **Decision**: Add endpoints under `/api/v1/media/reports/`
- Endpoints:
  - `GET /source-keywords/?platform={platform}` - List unique source_keywords
  - `POST /export-data/` - Get CSV-like data for Coze input
  - `POST /` - Create report
  - `GET /` - List reports
  - `GET /{id}/` - Get report detail
  - `DELETE /{id}/` - Delete report

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Large data exports may timeout | Limit export to max 500 records |
| Coze API rate limiting | Use existing timeout handling |
| Markdown XSS vulnerabilities | Use DOMPurify to sanitize rendered HTML |

## Open Questions

- None at this time

