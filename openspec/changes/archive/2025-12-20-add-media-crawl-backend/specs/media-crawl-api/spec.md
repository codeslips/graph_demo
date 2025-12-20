## ADDED Requirements

### Requirement: Media Crawl API Base URL
The system SHALL expose media crawl API endpoints under `/api/v1/media/`.

#### Scenario: API router mounted
- **WHEN** the application starts with `MEDIA_CRAWL_ENABLED=True`
- **THEN** the media crawl API router SHALL be mounted at `/api/v1/media/`

### Requirement: Bilibili API Endpoints
The system SHALL provide CRUD API endpoints for Bilibili platform models.

#### Scenario: List Bilibili videos
- **WHEN** `GET /api/v1/media/bilibili/videos/` is called
- **THEN** a paginated list of `BilibiliVideo` records SHALL be returned

#### Scenario: Create Bilibili video
- **WHEN** `POST /api/v1/media/bilibili/videos/` is called with valid payload
- **THEN** a new `BilibiliVideo` record SHALL be created and returned

#### Scenario: Get Bilibili video by ID
- **WHEN** `GET /api/v1/media/bilibili/videos/{id}/` is called
- **THEN** the matching `BilibiliVideo` record SHALL be returned

#### Scenario: Update Bilibili video
- **WHEN** `PUT /api/v1/media/bilibili/videos/{id}/` is called with valid payload
- **THEN** the `BilibiliVideo` record SHALL be updated and returned

#### Scenario: Delete Bilibili video
- **WHEN** `DELETE /api/v1/media/bilibili/videos/{id}/` is called
- **THEN** the `BilibiliVideo` record SHALL be deleted

#### Scenario: Bilibili video comments endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/bilibili/comments/`
- **THEN** `BilibiliVideoComment` records SHALL be managed accordingly

#### Scenario: Bilibili up info endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/bilibili/ups/`
- **THEN** `BilibiliUpInfo` records SHALL be managed accordingly

#### Scenario: Bilibili contact info endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/bilibili/contacts/`
- **THEN** `BilibiliContactInfo` records SHALL be managed accordingly

#### Scenario: Bilibili up dynamic endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/bilibili/dynamics/`
- **THEN** `BilibiliUpDynamic` records SHALL be managed accordingly

### Requirement: Douyin API Endpoints
The system SHALL provide CRUD API endpoints for Douyin platform models.

#### Scenario: Douyin aweme endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/douyin/awemes/`
- **THEN** `DouyinAweme` records SHALL be managed accordingly

#### Scenario: Douyin aweme comment endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/douyin/comments/`
- **THEN** `DouyinAwemeComment` records SHALL be managed accordingly

#### Scenario: Douyin creator endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/douyin/creators/`
- **THEN** `DyCreator` records SHALL be managed accordingly

### Requirement: Kuaishou API Endpoints
The system SHALL provide CRUD API endpoints for Kuaishou platform models.

#### Scenario: Kuaishou video endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/kuaishou/videos/`
- **THEN** `KuaishouVideo` records SHALL be managed accordingly

#### Scenario: Kuaishou video comment endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/kuaishou/comments/`
- **THEN** `KuaishouVideoComment` records SHALL be managed accordingly

### Requirement: Weibo API Endpoints
The system SHALL provide CRUD API endpoints for Weibo platform models.

#### Scenario: Weibo note endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/weibo/notes/`
- **THEN** `WeiboNote` records SHALL be managed accordingly

#### Scenario: Weibo note comment endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/weibo/comments/`
- **THEN** `WeiboNoteComment` records SHALL be managed accordingly

#### Scenario: Weibo creator endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/weibo/creators/`
- **THEN** `WeiboCreator` records SHALL be managed accordingly

### Requirement: Xiaohongshu API Endpoints
The system SHALL provide CRUD API endpoints for Xiaohongshu (XHS) platform models.

#### Scenario: XHS creator endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/xhs/creators/`
- **THEN** `XhsCreator` records SHALL be managed accordingly

#### Scenario: XHS note endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/xhs/notes/`
- **THEN** `XhsNote` records SHALL be managed accordingly

#### Scenario: XHS note comment endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/xhs/comments/`
- **THEN** `XhsNoteComment` records SHALL be managed accordingly

### Requirement: Tieba API Endpoints
The system SHALL provide CRUD API endpoints for Tieba platform models.

#### Scenario: Tieba note endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/tieba/notes/`
- **THEN** `TiebaNote` records SHALL be managed accordingly

#### Scenario: Tieba comment endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/tieba/comments/`
- **THEN** `TiebaComment` records SHALL be managed accordingly

#### Scenario: Tieba creator endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/tieba/creators/`
- **THEN** `TiebaCreator` records SHALL be managed accordingly

### Requirement: Zhihu API Endpoints
The system SHALL provide CRUD API endpoints for Zhihu platform models.

#### Scenario: Zhihu content endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/zhihu/contents/`
- **THEN** `ZhihuContent` records SHALL be managed accordingly

#### Scenario: Zhihu comment endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/zhihu/comments/`
- **THEN** `ZhihuComment` records SHALL be managed accordingly

#### Scenario: Zhihu creator endpoints
- **WHEN** CRUD operations are performed on `/api/v1/media/zhihu/creators/`
- **THEN** `ZhihuCreator` records SHALL be managed accordingly

### Requirement: Pagination
All list endpoints SHALL support pagination.

#### Scenario: Default pagination
- **WHEN** a list endpoint is called without pagination parameters
- **THEN** the first 20 records SHALL be returned with pagination metadata

#### Scenario: Custom pagination
- **WHEN** a list endpoint is called with `limit` and `offset` query parameters
- **THEN** the specified range of records SHALL be returned

### Requirement: Filtering
List endpoints SHALL support filtering by common fields.

#### Scenario: Filter by user_id
- **WHEN** a list endpoint is called with `user_id` query parameter
- **THEN** only records matching the specified `user_id` SHALL be returned

#### Scenario: Filter by create_time range
- **WHEN** a list endpoint is called with `create_time_from` and `create_time_to` query parameters
- **THEN** only records within the specified time range SHALL be returned

#### Scenario: Filter by source_keyword
- **WHEN** a list endpoint is called with `source_keyword` query parameter
- **THEN** only records matching the specified `source_keyword` SHALL be returned

### Requirement: Batch Operations
The system SHALL support batch create and delete operations.

#### Scenario: Batch create
- **WHEN** `POST /api/v1/media/{platform}/{resource}/batch/` is called with an array of records
- **THEN** multiple records SHALL be created in a single transaction

#### Scenario: Batch delete
- **WHEN** `DELETE /api/v1/media/{platform}/{resource}/batch/` is called with an array of IDs
- **THEN** multiple records SHALL be deleted in a single transaction

### Requirement: Error Responses
The API SHALL return consistent error responses.

#### Scenario: Resource not found
- **WHEN** a GET/PUT/DELETE operation targets a non-existent resource
- **THEN** a 404 Not Found response SHALL be returned with error details

#### Scenario: Validation error
- **WHEN** a POST/PUT operation is called with invalid payload
- **THEN** a 422 Unprocessable Entity response SHALL be returned with validation details

#### Scenario: Feature disabled
- **WHEN** any media crawl endpoint is called with `MEDIA_CRAWL_ENABLED=False`
- **THEN** a 503 Service Unavailable response SHALL be returned

