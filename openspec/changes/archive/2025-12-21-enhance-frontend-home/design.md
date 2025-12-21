# Design: Enhance Frontend Home Page

## Context

The current home page is a static landing page that provides no actionable information for users. To make the platform more user-friendly, we need to transform it into a functional dashboard that:
- Shows real-time platform statistics
- Guides users through the workflow
- Provides quick access to common actions
- Displays recent activity

## Goals / Non-Goals

### Goals
- Improve user onboarding by showing a clear workflow
- Provide quick access to all main features
- Show live statistics to give users context
- Display recent activity for quick access to ongoing work

### Non-Goals
- Creating a complex admin dashboard with charts/graphs
- Adding user authentication or personalized dashboards
- Real-time WebSocket updates (polling or on-mount fetch is sufficient)

## Decisions

### Decision 1: Component Structure
Split the home page into modular components for maintainability:
- `DashboardStats.vue` - Statistics cards
- `WorkflowGuide.vue` - 4-step workflow visualization
- `QuickActions.vue` - Action buttons grid
- `RecentActivity.vue` - Recent tasks and reports

**Alternative considered**: Single monolithic `HomeView.vue`
**Rationale**: Modular components improve readability, testability, and potential reuse.

### Decision 2: Data Fetching Strategy
Use existing APIs rather than creating new dashboard endpoints:
- Statistics: Aggregate from existing `/api/v1/media/` and `/api/v1/reports/` APIs
- Recent tasks: Use `/api/v1/crawl/status/` 
- Recent reports: Use `/api/v1/reports/?limit=5`

**Alternative considered**: Create dedicated `/api/v1/dashboard/` endpoint
**Rationale**: Reusing existing APIs avoids backend changes and keeps the change frontend-only.

### Decision 3: Loading States
Show skeleton loaders for statistics while data is fetching, rather than blocking the entire page.

**Rationale**: Improves perceived performance and allows users to see the page structure immediately.

## Visual Layout

```
┌────────────────────────────────────────────────────────────────┐
│  Dashboard Header                                              │
│  "旅游分析平台" + Brief description                              │
├────────────────────────────────────────────────────────────────┤
│  Statistics Row                                                │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐               │
│  │ 📊 数据 │  │ 🕷️ 任务 │  │ 📋 报告 │  │ 📱 平台 │               │
│  │  1,234  │  │   12   │  │   8    │  │   5    │               │
│  └────────┘  └────────┘  └────────┘  └────────┘               │
├────────────────────────────────────────────────────────────────┤
│  Workflow Guide                                                │
│  ┌──────┐  →  ┌──────┐  →  ┌──────┐  →  ┌──────┐              │
│  │  1   │     │  2   │     │  3   │     │  4   │              │
│  │爬虫  │     │数据  │     │报告  │     │图谱  │              │
│  └──────┘     └──────┘     └──────┘     └──────┘              │
├────────────────────────────────────────────────────────────────┤
│  Quick Actions                               Recent Activity   │
│  ┌─────────────────────────────┐   ┌─────────────────────────┐│
│  │ [🕷️ 启动爬虫] [📊 查看数据] │   │ Recent Tasks            ││
│  │ [📋 生成报告] [🕸️ 知识图谱] │   │ • Task 1 - Running      ││
│  │ [🤖 AI对话]                 │   │ • Task 2 - Done         ││
│  └─────────────────────────────┘   │ Recent Reports          ││
│                                     │ • Report 1 - 12/21      ││
│                                     │ • Report 2 - 12/20      ││
│                                     └─────────────────────────┘│
├────────────────────────────────────────────────────────────────┤
│  Feature Cards Grid                                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ 媒体爬虫 │  │ 数据管理 │  │ 分析报告 │  │ 知识图谱 │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                      ┌──────────┐                              │
│                      │ AI 对话  │                              │
│                      └──────────┘                              │
└────────────────────────────────────────────────────────────────┘
```

## Risks / Trade-offs

- **Risk**: Multiple API calls on page load may slow down initial render
  - **Mitigation**: Use loading skeletons, consider caching with Pinia store

- **Risk**: Statistics may become stale if user stays on page
  - **Mitigation**: Acceptable for MVP; can add refresh button or polling later

## Open Questions

- Should we cache dashboard data in a Pinia store or fetch fresh on each visit?
  - **Recommendation**: Fetch fresh on mount; simple and ensures accuracy

