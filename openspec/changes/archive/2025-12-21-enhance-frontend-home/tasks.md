# Tasks: Enhance Frontend Home Page

## 1. API & Data Layer

- [x] 1.1 Create dashboard statistics API endpoint or use existing APIs to fetch counts
- [x] 1.2 Create composable `useDashboard.ts` for dashboard data fetching
- [x] 1.3 Define TypeScript types for dashboard data

## 2. Dashboard Statistics Section

- [x] 2.1 Create statistics cards component showing:
  - Total media records count
  - Active/completed crawl tasks count
  - Generated reports count
  - Platforms with data count
- [x] 2.2 Implement loading states for statistics

## 3. Workflow Guide Section

- [x] 3.1 Create visual workflow diagram showing 4-step process:
  - Step 1: Configure & Start Crawler
  - Step 2: Manage Media Data  
  - Step 3: Generate Analysis Reports
  - Step 4: Explore Knowledge Graph
- [x] 3.2 Add clickable steps linking to respective pages

## 4. Quick Actions Section

- [x] 4.1 Create quick action buttons:
  - "启动爬虫任务" → `/media/crawl`
  - "查看媒体数据" → `/media`
  - "生成分析报告" → `/media` (opens report modal)
  - "探索知识图谱" → `/media-graph`
  - "AI 对话分析" → `/chat`

## 5. Recent Activity Section

- [x] 5.1 Display 3-5 most recent crawl task statuses
- [x] 5.2 Display 3-5 most recent analysis reports
- [x] 5.3 Add "查看全部" links to respective list pages

## 6. Feature Cards Section

- [x] 6.1 Redesign feature cards to be more actionable:
  - Media Crawler - with action button
  - Data Management - with action button
  - Analysis Reports - with action button
  - Knowledge Graph - with action button
  - AI Chat Assistant - with action button

## 7. Polish & Responsive

- [x] 7.1 Ensure consistent dark theme styling
- [x] 7.2 Add smooth animations for card hover and section load
- [x] 7.3 Test and fix responsive layout for mobile/tablet
