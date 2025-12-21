# Change: Enhance Frontend Home Page with Functional Dashboard

## Why

The current home page (`HomeView.vue`) is a static landing page that doesn't provide actionable guidance for users. Users need to understand the platform's core workflow (crawl → manage → analyze → visualize) and quickly access key features. A functional dashboard with live statistics, quick actions, and workflow guidance will improve user onboarding and platform usability.

## What Changes

- Replace static hero section with a dynamic dashboard overview
- Add live statistics cards showing data counts (total records, tasks, reports)
- Add quick action buttons for common workflows (start crawl, view data, generate report)
- Add a visual workflow guide explaining the platform's 4-step process
- Add recent activity section showing latest crawl tasks and reports
- Add feature navigation cards with direct links to key pages
- Maintain responsive design for mobile devices

## Impact

- **Affected specs**: Creates new `frontend-home` capability
- **Affected code**: 
  - `frontend/src/views/HomeView.vue` - Complete redesign
  - `frontend/src/api/` - May need new API calls for statistics
  - `frontend/src/stores/` - May need store for dashboard data

