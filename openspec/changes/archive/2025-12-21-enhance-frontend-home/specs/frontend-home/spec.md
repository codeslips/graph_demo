## ADDED Requirements

### Requirement: Dashboard Statistics Display
The home page SHALL display live statistics about the platform's data.

#### Scenario: Statistics cards visible on load
- **WHEN** the user visits the home page
- **THEN** statistics cards SHALL be displayed showing:
  - Total media records count across all platforms
  - Active or recent crawl tasks count
  - Generated analysis reports count
  - Number of platforms with data

#### Scenario: Statistics loading state
- **WHEN** statistics data is being fetched
- **THEN** loading indicators SHALL be displayed in place of numbers

#### Scenario: Statistics error handling
- **WHEN** statistics API fails to load
- **THEN** a graceful fallback (e.g., "-" or "N/A") SHALL be displayed

### Requirement: Workflow Guide Display
The home page SHALL display a visual guide explaining the platform's workflow.

#### Scenario: Workflow steps visible
- **WHEN** the user views the home page
- **THEN** a 4-step workflow guide SHALL be displayed:
  - Step 1: 配置并启动爬虫任务
  - Step 2: 管理媒体数据
  - Step 3: 生成分析报告
  - Step 4: 探索知识图谱

#### Scenario: Workflow step navigation
- **WHEN** the user clicks on a workflow step
- **THEN** the user SHALL be navigated to the corresponding page

### Requirement: Quick Actions
The home page SHALL provide quick action buttons for common operations.

#### Scenario: Quick action buttons displayed
- **WHEN** the user visits the home page
- **THEN** quick action buttons SHALL be displayed for:
  - Starting a new crawler task
  - Viewing media data
  - Generating analysis reports
  - Exploring knowledge graph
  - Opening AI chat

#### Scenario: Quick action navigation
- **WHEN** the user clicks a quick action button
- **THEN** the user SHALL be navigated to the appropriate page or action

### Requirement: Recent Activity Display
The home page SHALL display recent activity from the platform.

#### Scenario: Recent crawl tasks displayed
- **WHEN** the user visits the home page
- **THEN** the 3-5 most recent crawl tasks SHALL be displayed with their status

#### Scenario: Recent reports displayed
- **WHEN** the user visits the home page
- **THEN** the 3-5 most recent analysis reports SHALL be displayed

#### Scenario: View all links
- **WHEN** the user clicks "查看全部" link in the activity section
- **THEN** the user SHALL be navigated to the full list page

### Requirement: Feature Navigation Cards
The home page SHALL display feature cards that link to main platform functions.

#### Scenario: Feature cards displayed
- **WHEN** the user visits the home page
- **THEN** feature cards SHALL be displayed for:
  - 媒体爬虫 (Media Crawler)
  - 数据管理 (Data Management)
  - 分析报告 (Analysis Reports)
  - 知识图谱 (Knowledge Graph)
  - AI 对话 (AI Chat)

#### Scenario: Feature card interaction
- **WHEN** the user clicks a feature card
- **THEN** the user SHALL be navigated to the corresponding page

#### Scenario: Feature card hover effect
- **WHEN** the user hovers over a feature card
- **THEN** a visual feedback (transform, border glow) SHALL be applied

### Requirement: Responsive Layout
The home page SHALL be responsive across different screen sizes.

#### Scenario: Desktop layout
- **WHEN** the viewport width is >= 1024px
- **THEN** multi-column layouts SHALL be used for statistics and feature cards

#### Scenario: Tablet layout
- **WHEN** the viewport width is between 768px and 1023px
- **THEN** reduced column layouts (2 columns) SHALL be used

#### Scenario: Mobile layout
- **WHEN** the viewport width is < 768px
- **THEN** single-column stacked layout SHALL be used

