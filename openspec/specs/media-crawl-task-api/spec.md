# media-crawl-task-api Specification

## Purpose
TBD - created by archiving change add-media-crawl-task. Update Purpose after archive.
## Requirements
### Requirement: Media Crawl Service URL Configuration
The system SHALL read the external media crawl service URL from environment variable `MEDIA_CRAWL_SERVICE_URL`.

#### Scenario: Environment variable configured
- **WHEN** the application starts with `MEDIA_CRAWL_SERVICE_URL=http://localhost:8777`
- **THEN** the backend SHALL use this URL to proxy requests to the external crawler service

#### Scenario: Environment variable not set
- **WHEN** the application starts without `MEDIA_CRAWL_SERVICE_URL`
- **THEN** the default value SHALL be `http://localhost:8777`

### Requirement: Start Crawler Task Endpoint
The system SHALL provide an endpoint to start a new crawler task via the external service.

#### Scenario: Start crawler task successfully
- **WHEN** `POST /api/v1/media/crawler/start` is called with valid payload
- **THEN** the request SHALL be proxied to `{MEDIA_CRAWL_SERVICE_URL}/api/crawler/start`
- **AND** the response from the external service SHALL be returned

#### Scenario: Start crawler request payload
- **WHEN** starting a crawler task
- **THEN** the payload SHALL accept the following fields:
  - `platform` (string, required): Platform to crawl (xhs, douyin, bilibili, etc.)
  - `login_type` (string, required): Login method (qrcode, cookie)
  - `crawler_type` (string, required): Type of crawl (search, detail, creator)
  - `keywords` (string, optional): Search keywords
  - `specified_ids` (string, optional): Specific content IDs to crawl
  - `creator_ids` (string, optional): Creator IDs to crawl
  - `start_page` (integer, optional): Starting page number
  - `enable_comments` (boolean, optional): Whether to crawl comments
  - `enable_sub_comments` (boolean, optional): Whether to crawl sub-comments
  - `save_option` (string, optional): Save option (db)
  - `cookies` (string, optional): Custom cookies
  - `headless` (boolean, optional): Run browser in headless mode

#### Scenario: External service unavailable
- **WHEN** `POST /api/v1/media/crawler/start` is called
- **AND** the external crawler service is not reachable
- **THEN** a 503 Service Unavailable response SHALL be returned with error details

### Requirement: Get Crawler Status Endpoint
The system SHALL provide an endpoint to get the current crawler task status.

#### Scenario: Get crawler status successfully
- **WHEN** `GET /api/v1/media/crawler/status` is called
- **THEN** the request SHALL be proxied to `{MEDIA_CRAWL_SERVICE_URL}/api/crawler/status`
- **AND** the response SHALL include: status, platform, crawler_type, started_at, error_message

#### Scenario: Status response values
- **WHEN** a crawler task is running
- **THEN** the status field SHALL be one of: `running`, `idle`

#### Scenario: External service unavailable for status
- **WHEN** `GET /api/v1/media/crawler/status` is called
- **AND** the external crawler service is not reachable
- **THEN** a 503 Service Unavailable response SHALL be returned

### Requirement: Feature Toggle
The system SHALL respect the existing `MEDIA_CRAWL_ENABLED` setting.

#### Scenario: Feature disabled
- **WHEN** any crawler endpoint is called with `MEDIA_CRAWL_ENABLED=False`
- **THEN** a 503 Service Unavailable response SHALL be returned

