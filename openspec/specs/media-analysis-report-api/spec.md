# media-analysis-report-api Specification

## Purpose
TBD - created by archiving change add-media-analysis-report. Update Purpose after archive.
## Requirements
### Requirement: Analysis Report Model

The system SHALL provide an `AnalysisReport` model to persist generated analysis reports with the following fields:
- `id` (UUID, primary key)
- `title` (string, auto-generated or user-provided)
- `platform` (string, the source platform e.g., "xhs", "douyin")
- `source_keyword` (string, the keyword used to filter data)
- `time_from` (timestamp, start of time range filter)
- `time_to` (timestamp, end of time range filter)
- `content` (text, the markdown content of the report)
- `record_count` (integer, number of records analyzed)
- `created_at` (timestamp, when the report was created)

#### Scenario: Report created with all fields
- **WHEN** a report is created with valid data
- **THEN** all fields SHALL be persisted to the database
- **AND** `created_at` SHALL be auto-populated with current timestamp

### Requirement: Source Keywords List API

The system SHALL provide an API endpoint `GET /api/v1/media/reports/source-keywords/` to list unique source_keyword values from media data.

#### Scenario: Get source keywords for platform
- **WHEN** `GET /api/v1/media/reports/source-keywords/?platform=xhs` is called
- **THEN** a list of unique `source_keyword` values from XhsNote table SHALL be returned
- **AND** the list SHALL be sorted alphabetically

#### Scenario: Filter by platform
- **WHEN** the `platform` query parameter is provided
- **THEN** only source_keywords from that platform's content model SHALL be returned

#### Scenario: Empty result
- **WHEN** no records exist for the specified platform
- **THEN** an empty list SHALL be returned

### Requirement: Data Export API

The system SHALL provide an API endpoint `POST /api/v1/media/reports/export-data/` to export filtered media data in CSV-like format.

#### Scenario: Export data with filters
- **WHEN** `POST /api/v1/media/reports/export-data/` is called with:
  ```json
  {
    "platform": "xhs",
    "source_keyword": "三亚旅游",
    "time_from": 1688140800,
    "time_to": 1696118400
  }
  ```
- **THEN** the response SHALL contain CSV-like text data with header row and data rows
- **AND** data SHALL be filtered by source_keyword and time range (using `time` field)

#### Scenario: Export format for XHS
- **WHEN** platform is "xhs"
- **THEN** the exported data SHALL include columns: `note_id,title,desc,liked_count,collected_count,comment_count,share_count,time,user_id,nickname,ip_location,tag_list`

#### Scenario: Export limit
- **WHEN** more than 500 records match the filter
- **THEN** only the first 500 records SHALL be exported
- **AND** the response SHALL indicate the total count and that data was truncated

#### Scenario: Source keyword not found
- **WHEN** the provided source_keyword does not exist in the database
- **THEN** a 404 Not Found response SHALL be returned with error message

### Requirement: Create Report API

The system SHALL provide an API endpoint `POST /api/v1/media/reports/` to create a new analysis report.

#### Scenario: Create report
- **WHEN** `POST /api/v1/media/reports/` is called with valid report data
- **THEN** a new `AnalysisReport` record SHALL be created
- **AND** the created report SHALL be returned with its ID

#### Scenario: Validation error
- **WHEN** required fields are missing
- **THEN** a 422 Unprocessable Entity response SHALL be returned

### Requirement: List Reports API

The system SHALL provide an API endpoint `GET /api/v1/media/reports/` to list saved analysis reports.

#### Scenario: List reports with pagination
- **WHEN** `GET /api/v1/media/reports/` is called
- **THEN** a paginated list of reports SHALL be returned
- **AND** reports SHALL be ordered by `created_at` descending (newest first)

#### Scenario: Filter by platform
- **WHEN** `GET /api/v1/media/reports/?platform=xhs` is called
- **THEN** only reports for the specified platform SHALL be returned

### Requirement: Get Report Detail API

The system SHALL provide an API endpoint `GET /api/v1/media/reports/{id}/` to get a single report.

#### Scenario: Get existing report
- **WHEN** `GET /api/v1/media/reports/{id}/` is called with valid ID
- **THEN** the full report including content SHALL be returned

#### Scenario: Report not found
- **WHEN** the specified ID does not exist
- **THEN** a 404 Not Found response SHALL be returned

### Requirement: Delete Report API

The system SHALL provide an API endpoint `DELETE /api/v1/media/reports/{id}/` to delete a report.

#### Scenario: Delete existing report
- **WHEN** `DELETE /api/v1/media/reports/{id}/` is called with valid ID
- **THEN** the report SHALL be deleted from the database
- **AND** a 204 No Content response SHALL be returned

#### Scenario: Delete non-existent report
- **WHEN** the specified ID does not exist
- **THEN** a 404 Not Found response SHALL be returned

