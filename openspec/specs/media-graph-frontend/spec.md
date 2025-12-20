# media-graph-frontend Specification

## Purpose
TBD - created by archiving change add-media-neo4j-sync. Update Purpose after archive.
## Requirements
### Requirement: Media Graph View Page

The system SHALL provide a dedicated page for viewing media graph data.

#### Scenario: Navigate to media graph

- **WHEN** user navigates to `/media-graph`
- **THEN** the media graph view page SHALL be displayed
- **AND** graph data SHALL be fetched from the API

#### Scenario: Display loading state

- **GIVEN** graph data is being fetched
- **WHEN** the page loads
- **THEN** a loading indicator SHALL be displayed

#### Scenario: Display empty state

- **GIVEN** no media data has been synced to Neo4j
- **WHEN** the page loads
- **THEN** an empty state message SHALL be displayed
- **AND** a prompt to sync data SHALL be shown

### Requirement: Platform Filter Tabs

The system SHALL provide tabs to filter graph data by platform.

#### Scenario: Display platform tabs

- **WHEN** the media graph page loads
- **THEN** tabs for all 7 platforms (Bilibili, Douyin, Kuaishou, Weibo, XHS, Tieba, Zhihu) SHALL be displayed
- **AND** an "All Platforms" tab SHALL be available

#### Scenario: Switch platform filter

- **WHEN** user clicks a platform tab
- **THEN** the graph SHALL reload with data filtered by the selected platform

#### Scenario: Default to all platforms

- **WHEN** the page first loads
- **THEN** the "All Platforms" tab SHALL be selected by default

### Requirement: Keyword Search and Tag Cloud

The system SHALL provide keyword-based graph exploration.

#### Scenario: Display keyword cloud

- **WHEN** the media graph page loads
- **THEN** a cloud of popular keywords SHALL be displayed in the sidebar
- **AND** keywords SHALL be sized by content count

#### Scenario: Click keyword in cloud

- **WHEN** user clicks a keyword in the tag cloud
- **THEN** the graph SHALL reload showing content related to that keyword
- **AND** related keywords SHALL be highlighted

#### Scenario: Search keywords

- **WHEN** user types in the keyword search input (minimum 2 characters)
- **THEN** matching keywords SHALL be displayed as search results
- **AND** user can click a result to filter the graph

#### Scenario: Clear keyword filter

- **WHEN** user clicks the clear filter button
- **THEN** the graph SHALL reload showing all content for the current platform filter

### Requirement: Graph Canvas Integration

The system SHALL reuse existing graph visualization components.

#### Scenario: Render media graph

- **WHEN** media graph data is loaded
- **THEN** the GraphCanvas component SHALL render the force-directed graph
- **AND** Content nodes SHALL be displayed with platform-specific colors
- **AND** Keyword nodes SHALL be displayed with distinct color
- **AND** Comment nodes SHALL be displayed with distinct color

#### Scenario: Node visual differentiation by platform

- **WHEN** the graph is rendered
- **THEN** Bilibili content nodes SHALL have a distinct color
- **AND** Douyin content nodes SHALL have a different color
- **AND** each platform SHALL have a unique visual style

#### Scenario: Graph interaction

- **WHEN** user interacts with the graph
- **THEN** nodes SHALL be draggable
- **AND** graph SHALL be zoomable via scroll
- **AND** graph SHALL be pannable via drag

### Requirement: Node Detail Panel

The system SHALL display detailed information when a node is selected.

#### Scenario: Show content node details

- **WHEN** user clicks a Content node
- **THEN** a detail panel SHALL appear
- **AND** panel SHALL show title, author, platform, create time
- **AND** panel SHALL include a link to the original content URL

#### Scenario: Show keyword node details

- **WHEN** user clicks a Keyword node
- **THEN** panel SHALL show keyword name and count of related content
- **AND** panel SHALL list platforms where this keyword appears

#### Scenario: Show comment node details

- **WHEN** user clicks a Comment node
- **THEN** panel SHALL show comment content, author, create time

#### Scenario: Dismiss panel

- **WHEN** user clicks outside the detail panel
- **THEN** the panel SHALL close

### Requirement: Sync Trigger Button

The system SHALL provide a manual sync trigger on the media page.

#### Scenario: Display sync button

- **WHEN** user views the media management page (`/media`)
- **THEN** a "Sync to Neo4j" button SHALL be displayed in the header

#### Scenario: Trigger sync

- **WHEN** user clicks the "Sync to Neo4j" button
- **THEN** the system SHALL call the sync API endpoint
- **AND** a loading indicator SHALL be displayed on the button
- **AND** the button SHALL be disabled during sync

#### Scenario: Sync completion notification

- **WHEN** the sync operation completes
- **THEN** a success notification SHALL be displayed with sync statistics
- **AND** the button SHALL return to enabled state

#### Scenario: Sync error notification

- **WHEN** the sync operation fails
- **THEN** an error notification SHALL be displayed with error message

### Requirement: Navigation Link

The system SHALL provide navigation to the media graph page.

#### Scenario: Sidebar navigation

- **WHEN** user views any page in the application
- **THEN** a "媒体图谱" (Media Graph) navigation link SHALL be visible in the sidebar

#### Scenario: Navigate from media page

- **WHEN** user clicks "View Graph" link on the media page
- **THEN** user SHALL be navigated to `/media-graph`

### Requirement: Graph Legend

The system SHALL display a legend for the media graph.

#### Scenario: Display legend

- **WHEN** the media graph is displayed
- **THEN** a legend SHALL show node types with their colors
- **AND** legend SHALL include: Platform, Content (per platform), Keyword, Comment

#### Scenario: Display statistics

- **WHEN** the graph is displayed
- **THEN** the legend SHALL show total node counts by type
- **AND** the legend SHALL show total edge count

