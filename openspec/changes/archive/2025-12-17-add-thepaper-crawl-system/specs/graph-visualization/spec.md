# graph-visualization Specification

## Purpose

Provides interactive graph visualization in the Vue frontend using ECharts to display news article relationships.

## ADDED Requirements

### Requirement: Graph Canvas Component

The system SHALL provide an ECharts-based graph visualization component.

#### Scenario: Render force-directed graph

- **GIVEN** graph data with nodes and edges
- **WHEN** the GraphCanvas component mounts
- **THEN** it SHALL render a force-directed layout using ECharts
- **AND** nodes SHALL be positioned using physics simulation
- **AND** edges SHALL connect related nodes

#### Scenario: Node visual differentiation

- **WHEN** the graph is rendered
- **THEN** Article nodes SHALL be displayed with one color and size
- **AND** Channel nodes SHALL be displayed with a different color
- **AND** Tag nodes SHALL be displayed with a distinct color
- **AND** a legend SHALL indicate node types

#### Scenario: Graph interaction

- **WHEN** user interacts with the graph
- **THEN** nodes SHALL be draggable
- **AND** graph SHALL be zoomable via scroll
- **AND** graph SHALL be pannable via drag

### Requirement: Node Detail Panel

The system SHALL display detailed information when a node is selected.

#### Scenario: Show article details

- **WHEN** user clicks an Article node
- **THEN** a detail panel SHALL appear
- **AND** panel SHALL show title, author, publish time, summary
- **AND** panel SHALL include a link to the original article

#### Scenario: Show tag details

- **WHEN** user clicks a Tag node
- **THEN** panel SHALL show tag name and count of related articles

#### Scenario: Dismiss panel

- **WHEN** user clicks outside the detail panel
- **THEN** the panel SHALL close

### Requirement: Task Management UI

The system SHALL provide a UI for creating and monitoring crawl tasks.

#### Scenario: Create crawl task form

- **WHEN** user visits the task list page
- **THEN** a form SHALL be displayed with target URL input
- **AND** form SHALL have a crawl type selector
- **AND** form SHALL have a submit button

#### Scenario: Submit crawl task

- **WHEN** user submits the form with valid input
- **THEN** API request SHALL be sent to create task
- **AND** form SHALL show loading state during submission
- **AND** new task SHALL appear in task list after creation

#### Scenario: Display task list

- **WHEN** user visits the task list page
- **THEN** existing tasks SHALL be displayed in a list
- **AND** each task SHALL show status, title, created time
- **AND** tasks SHALL be ordered by created time descending

#### Scenario: Task status indicator

- **WHEN** task list is displayed
- **THEN** PENDING tasks SHALL show a waiting indicator
- **AND** RUNNING tasks SHALL show a progress indicator
- **AND** DONE tasks SHALL show a success indicator
- **AND** FAILED tasks SHALL show an error indicator

### Requirement: Graph View Page

The system SHALL provide a dedicated page for viewing task graphs.

#### Scenario: Navigate to graph view

- **WHEN** user clicks "View Graph" on a completed task
- **THEN** browser SHALL navigate to `/graph/{taskId}`
- **AND** graph data SHALL be fetched from API
- **AND** GraphCanvas SHALL render the data

#### Scenario: Loading state

- **GIVEN** graph data is being fetched
- **WHEN** the graph view loads
- **THEN** a loading indicator SHALL be displayed
- **AND** loading SHALL disappear when data arrives

#### Scenario: Error state

- **GIVEN** graph API returns an error
- **WHEN** the graph view loads
- **THEN** an error message SHALL be displayed
- **AND** a retry button SHALL be available

### Requirement: Real-time Task Status

The system SHALL update task status in real-time during crawl execution.

#### Scenario: Poll for task updates

- **GIVEN** a task is in RUNNING status
- **WHEN** the task list is displayed
- **THEN** the system SHALL poll the API every 3 seconds
- **AND** task status SHALL update when changed
- **AND** polling SHALL stop when task reaches DONE or FAILED

