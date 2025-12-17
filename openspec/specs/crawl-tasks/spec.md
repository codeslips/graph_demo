# crawl-tasks Specification

## Purpose
TBD - created by archiving change add-thepaper-crawl-system. Update Purpose after archive.
## Requirements
### Requirement: Crawl Task Model

The system SHALL provide a `CrawlTask` Django model to track crawl job execution.

#### Scenario: Create a new crawl task

- **WHEN** a user submits a crawl request via API
- **THEN** a `CrawlTask` record SHALL be created with status `PENDING`
- **AND** the task SHALL have a unique UUID identifier
- **AND** the task SHALL store `target_url`, `crawl_type`, and `created_at`

#### Scenario: Task status transitions

- **GIVEN** a CrawlTask in `PENDING` status
- **WHEN** the Celery worker picks up the task
- **THEN** the status SHALL transition to `RUNNING`
- **AND** `started_at` timestamp SHALL be set
- **WHEN** the crawl completes successfully
- **THEN** the status SHALL transition to `DONE`
- **AND** `finished_at` timestamp SHALL be set
- **WHEN** the crawl fails with an error
- **THEN** the status SHALL transition to `FAILED`
- **AND** `error_message` SHALL contain the error details

### Requirement: Crawl Item Model

The system SHALL provide a `CrawlItem` model to store individual crawled articles.

#### Scenario: Store crawled article

- **WHEN** an article is successfully parsed
- **THEN** a `CrawlItem` record SHALL be created
- **AND** it SHALL store `title`, `url`, `author`, `publish_time`, `summary`, `category`
- **AND** it SHALL have a foreign key to the parent `CrawlTask`
- **AND** `neo4j_synced` flag SHALL be `False` initially

### Requirement: Celery Async Crawl Execution

The system SHALL execute crawl operations asynchronously via Celery.

#### Scenario: Dispatch crawl task

- **WHEN** a CrawlTask is created via API
- **THEN** a Celery task SHALL be dispatched
- **AND** the HTTP response SHALL return immediately with task ID
- **AND** the crawl SHALL execute in background

#### Scenario: Crawl channel news list

- **GIVEN** a crawl task with `crawl_type=news_list`
- **WHEN** the Celery worker executes the task
- **THEN** it SHALL fetch the channel content from ThePaper API
- **AND** it SHALL parse each article's detail page
- **AND** it SHALL create CrawlItem records for each article
- **AND** it SHALL sync data to Neo4j after all items are saved

### Requirement: Crawl Task API

The system SHALL provide REST API endpoints for crawl task management.

#### Scenario: Create crawl task via API

- **WHEN** POST request to `/api/v1/crawl/tasks` with valid payload
- **THEN** response SHALL return 201 with task details
- **AND** the task SHALL be created in database
- **AND** the Celery task SHALL be dispatched

#### Scenario: List crawl tasks

- **WHEN** GET request to `/api/v1/crawl/tasks`
- **THEN** response SHALL return paginated list of tasks
- **AND** tasks SHALL be ordered by `created_at` descending

#### Scenario: Get task details

- **WHEN** GET request to `/api/v1/crawl/tasks/{id}`
- **THEN** response SHALL return task details including status and item count
- **WHEN** task ID does not exist
- **THEN** response SHALL return 404

#### Scenario: Delete crawl task

- **WHEN** DELETE request to `/api/v1/crawl/tasks/{id}`
- **THEN** the task and associated items SHALL be deleted
- **AND** response SHALL return 204

