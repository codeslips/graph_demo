# media-analysis-report-frontend Specification

## Purpose
TBD - created by archiving change add-media-analysis-report. Update Purpose after archive.
## Requirements
### Requirement: Generate Report Button

The system SHALL provide a "生成分析报告" button in the MediaView header actions area.

#### Scenario: Button displayed
- **WHEN** the user views the MediaView page
- **THEN** a "生成分析报告" button SHALL be visible in the header actions

#### Scenario: Button click opens modal
- **WHEN** the user clicks the "生成分析报告" button
- **THEN** the Report Generator Modal SHALL open

### Requirement: Report Generator Modal

The system SHALL provide a modal dialog for configuring and generating analysis reports.

#### Scenario: Modal layout
- **WHEN** the Report Generator Modal opens
- **THEN** it SHALL display:
  - Source keyword input field
  - Time range picker (from date and to date)
  - "生成报告" (Generate Report) button
  - Close/cancel button

#### Scenario: Source keyword input with validation
- **WHEN** the user types in the source keyword input
- **THEN** suggestions from existing source_keywords SHALL be shown
- **AND** if the entered keyword does not exist, an error message SHALL be displayed

#### Scenario: Generate report flow
- **WHEN** the user enters valid source_keyword, selects time range, and clicks "生成报告"
- **THEN** the system SHALL:
  1. Call the export-data API to get CSV-like data
  2. Send the data to Coze API
  3. Display streaming response in a preview area
  4. Show "保存报告" button when generation completes

#### Scenario: Loading state during generation
- **WHEN** report generation is in progress
- **THEN** a loading indicator SHALL be displayed
- **AND** the generate button SHALL be disabled

#### Scenario: Report preview with markdown
- **WHEN** the Coze API returns report content
- **THEN** the content SHALL be rendered as formatted HTML from markdown

### Requirement: Save Report

The system SHALL allow users to save generated reports.

#### Scenario: Save report button
- **WHEN** report generation completes successfully
- **THEN** a "保存报告" button SHALL be displayed

#### Scenario: Save report action
- **WHEN** the user clicks "保存报告"
- **THEN** the report SHALL be saved via the create report API
- **AND** a success message SHALL be displayed
- **AND** the modal MAY close or allow generating another report

### Requirement: Report List Navigation

The system SHALL provide navigation to the report list page.

#### Scenario: Navigation link displayed
- **WHEN** the user views any page in the application
- **THEN** a "报告列表" navigation link SHALL be visible in the main navigation

#### Scenario: Navigate to report list
- **WHEN** the user clicks the "报告列表" link
- **THEN** the user SHALL be navigated to `/reports`

### Requirement: Report List View

The system SHALL provide a page to view all saved reports.

#### Scenario: Display report list
- **WHEN** the user visits `/reports`
- **THEN** a list of saved reports SHALL be displayed with:
  - Report title
  - Platform
  - Source keyword
  - Created date
  - Delete button

#### Scenario: Pagination
- **WHEN** there are more than 20 reports
- **THEN** pagination controls SHALL be displayed

#### Scenario: Click to view detail
- **WHEN** the user clicks on a report row
- **THEN** the user SHALL be navigated to `/reports/{id}`

#### Scenario: Delete report
- **WHEN** the user clicks the delete button on a report
- **THEN** a confirmation dialog SHALL be displayed
- **AND** upon confirmation, the report SHALL be deleted
- **AND** the list SHALL refresh

#### Scenario: Empty state
- **WHEN** no reports exist
- **THEN** an empty state message SHALL be displayed

### Requirement: Report Detail View

The system SHALL provide a page to view a single report's content.

#### Scenario: Display report detail
- **WHEN** the user visits `/reports/{id}`
- **THEN** the page SHALL display:
  - Report title
  - Platform and source keyword
  - Time range (from - to)
  - Record count analyzed
  - Created date
  - Report content rendered as HTML from markdown

#### Scenario: Markdown rendering
- **WHEN** report content contains markdown syntax
- **THEN** it SHALL be rendered as properly formatted HTML
- **AND** the HTML SHALL be sanitized to prevent XSS

#### Scenario: Back navigation
- **WHEN** the user clicks the back button
- **THEN** the user SHALL be navigated back to `/reports`

#### Scenario: Report not found
- **WHEN** the specified report ID does not exist
- **THEN** a 404 error message SHALL be displayed

### Requirement: Error Handling

The system SHALL display appropriate error messages for all failure scenarios.

#### Scenario: Export data error
- **WHEN** the export-data API returns an error
- **THEN** an error message SHALL be displayed in the modal

#### Scenario: Coze API error
- **WHEN** the Coze API fails to generate a report
- **THEN** an error message SHALL be displayed
- **AND** the user SHALL be able to retry

#### Scenario: Save report error
- **WHEN** saving the report fails
- **THEN** an error message SHALL be displayed
- **AND** the report content SHALL remain visible for retry

