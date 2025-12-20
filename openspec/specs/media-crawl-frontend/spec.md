# media-crawl-frontend Specification

## Purpose
TBD - created by archiving change add-media-crawl-frontend. Update Purpose after archive.
## Requirements
### Requirement: Media Management Navigation
The system SHALL provide a navigation link to access the media management page.

#### Scenario: Navigation link displayed
- **WHEN** the user views any page in the application
- **THEN** a "媒体数据" navigation link SHALL be visible in the main navigation bar

#### Scenario: Navigation to media page
- **WHEN** the user clicks the "媒体数据" navigation link
- **THEN** the user SHALL be navigated to `/media`

### Requirement: Platform Tab Navigation
The system SHALL provide tabbed navigation to switch between different social media platforms.

#### Scenario: Display platform tabs
- **WHEN** the user visits the media management page
- **THEN** tabs for all 7 platforms (Bilibili, Douyin, Kuaishou, Weibo, XHS, Tieba, Zhihu) SHALL be displayed

#### Scenario: Switch platform tab
- **WHEN** the user clicks a platform tab
- **THEN** the data table SHALL display records for the selected platform

#### Scenario: Remember selected platform
- **WHEN** the user returns to the media page after navigation
- **THEN** the last selected platform tab SHALL be restored

### Requirement: Data Table Display
The system SHALL display platform data in a paginated table format.

#### Scenario: Display paginated data
- **WHEN** the user views a platform tab
- **THEN** records SHALL be displayed in a table with pagination controls

#### Scenario: Default pagination
- **WHEN** the page first loads
- **THEN** the first 20 records SHALL be displayed

#### Scenario: Change page
- **WHEN** the user clicks a pagination control
- **THEN** the corresponding page of records SHALL be loaded and displayed

### Requirement: Data Filtering
The system SHALL allow users to filter data by common fields.

#### Scenario: Filter by user_id
- **WHEN** the user enters a user_id in the filter input
- **THEN** only records matching the user_id SHALL be displayed

#### Scenario: Filter by date range
- **WHEN** the user selects a date range
- **THEN** only records within that time range SHALL be displayed

#### Scenario: Filter by source keyword
- **WHEN** the user enters a source keyword
- **THEN** only records matching the keyword SHALL be displayed

#### Scenario: Clear filters
- **WHEN** the user clicks the clear filters button
- **THEN** all filter inputs SHALL be reset and all records SHALL be displayed

### Requirement: Create Record
The system SHALL allow users to create new records.

#### Scenario: Open create modal
- **WHEN** the user clicks the "新建" (Create) button
- **THEN** a modal form with fields for the current platform entity SHALL be displayed

#### Scenario: Submit create form
- **WHEN** the user fills in the form and clicks submit
- **THEN** a new record SHALL be created via the API and the table SHALL refresh

#### Scenario: Cancel create
- **WHEN** the user clicks cancel on the create modal
- **THEN** the modal SHALL close without creating a record

### Requirement: Edit Record
The system SHALL allow users to edit existing records.

#### Scenario: Open edit modal
- **WHEN** the user clicks the edit button on a table row
- **THEN** a modal form pre-filled with the record data SHALL be displayed

#### Scenario: Submit edit form
- **WHEN** the user modifies fields and clicks submit
- **THEN** the record SHALL be updated via the API and the table SHALL refresh

### Requirement: Delete Record
The system SHALL allow users to delete individual records.

#### Scenario: Confirm single delete
- **WHEN** the user clicks the delete button on a table row
- **THEN** a confirmation dialog SHALL be displayed

#### Scenario: Execute single delete
- **WHEN** the user confirms the delete action
- **THEN** the record SHALL be deleted via the API and removed from the table

#### Scenario: Cancel delete
- **WHEN** the user cancels the delete action
- **THEN** the record SHALL remain unchanged

### Requirement: Batch Delete
The system SHALL allow users to delete multiple records at once.

#### Scenario: Select multiple records
- **WHEN** the user checks multiple row checkboxes
- **THEN** the batch delete button SHALL become enabled

#### Scenario: Confirm batch delete
- **WHEN** the user clicks the batch delete button
- **THEN** a confirmation dialog showing the count of selected records SHALL be displayed

#### Scenario: Execute batch delete
- **WHEN** the user confirms the batch delete
- **THEN** all selected records SHALL be deleted via the API and removed from the table

### Requirement: View Record Detail
The system SHALL allow users to view detailed information for a single record.

#### Scenario: Navigate to detail view
- **WHEN** the user clicks on a record row or a view detail button
- **THEN** the user SHALL be navigated to `/media/:platform/:entityType/:id`

#### Scenario: Display full record data
- **WHEN** the user views the detail page
- **THEN** all fields of the record SHALL be displayed in a formatted layout

### Requirement: Loading States
The system SHALL display appropriate loading indicators during API operations.

#### Scenario: Table loading
- **WHEN** data is being fetched from the API
- **THEN** a loading spinner SHALL be displayed in the table area

#### Scenario: Action loading
- **WHEN** a create/update/delete operation is in progress
- **THEN** the submit button SHALL show a loading state and be disabled

### Requirement: Error Handling
The system SHALL display user-friendly error messages when API operations fail.

#### Scenario: API error display
- **WHEN** an API request fails
- **THEN** an error message SHALL be displayed to the user

#### Scenario: Feature disabled error
- **WHEN** the media crawl feature is disabled on the backend
- **THEN** an appropriate message SHALL be displayed indicating the feature is unavailable

