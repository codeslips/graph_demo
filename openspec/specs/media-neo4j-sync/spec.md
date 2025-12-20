# media-neo4j-sync Specification

## Purpose
TBD - created by archiving change add-media-neo4j-sync. Update Purpose after archive.
## Requirements
### Requirement: Media Neo4j Graph Model

The system SHALL create Neo4j nodes and relationships for media content using a content-centric model.

#### Scenario: Create Platform node

- **WHEN** syncing media data for a platform
- **THEN** a Platform node SHALL be created with `name` property
- **AND** duplicate Platform nodes SHALL be merged by `name`

#### Scenario: Create Content node

- **WHEN** syncing a video, note, or post from any platform
- **THEN** a Content node SHALL be created with properties: `contentId`, `platform`, `contentType`, `title`, `author`, `url`, `createTime`
- **AND** duplicate Content nodes SHALL be merged by `platform` + `contentId` composite key
- **AND** a `HAS_CONTENT` relationship SHALL link Platform to Content

#### Scenario: Create Keyword node from source_keyword

- **WHEN** syncing content with a non-empty `source_keyword` field
- **THEN** a Keyword node SHALL be created with `name` property
- **AND** a `HAS_KEYWORD` relationship SHALL link Content to Keyword

#### Scenario: Create Keyword node from hashtags

- **WHEN** syncing content with hashtags in title or description (pattern: `#keyword#` or `#keyword `)
- **THEN** Keyword nodes SHALL be created for each extracted hashtag
- **AND** `HAS_KEYWORD` relationships SHALL link Content to each Keyword

#### Scenario: Create Comment node

- **WHEN** syncing comments for content
- **THEN** Comment nodes SHALL be created with properties: `commentId`, `content`, `author`, `createTime`
- **AND** a `HAS_COMMENT` relationship SHALL link Content to Comment

### Requirement: Manual Sync Trigger

The system SHALL provide a manual trigger to sync media data to Neo4j.

#### Scenario: Sync all platforms

- **WHEN** a POST request is made to `/api/v1/media/sync-neo4j` without platform parameter
- **THEN** the system SHALL queue a Celery task to sync all 6 supported platforms
- **AND** the response SHALL include a `task_id` for tracking

#### Scenario: Sync specific platform

- **WHEN** a POST request is made to `/api/v1/media/sync-neo4j` with `platform` parameter
- **THEN** the system SHALL queue a Celery task to sync only the specified platform
- **AND** the response SHALL include a `task_id` for tracking

#### Scenario: Sync with limit

- **WHEN** a POST request includes a `limit` parameter
- **THEN** the sync SHALL process at most `limit` content items per platform

### Requirement: Sync Status Tracking

The system SHALL provide sync operation status.

#### Scenario: Get sync status

- **WHEN** a GET request is made to `/api/v1/media/sync-status`
- **THEN** the response SHALL include: `lastSyncTime`, `totalContentSynced`, `totalKeywordsSynced`, `status` (idle/running)

#### Scenario: Sync progress during operation

- **WHEN** a sync task is running
- **THEN** the status endpoint SHALL return `status: "running"` with `progress` percentage

### Requirement: Media Graph Data Retrieval

The system SHALL provide API endpoints to fetch media graph data from Neo4j.

#### Scenario: Get graph by platform

- **WHEN** a GET request is made to `/api/v1/graph/media?platform=bilibili`
- **THEN** the response SHALL include nodes and edges for the specified platform
- **AND** the response SHALL include statistics (node counts by type, edge counts)

#### Scenario: Get graph by keyword

- **WHEN** a GET request is made to `/api/v1/graph/media?keyword=游戏`
- **THEN** the response SHALL include all Content nodes linked to the specified Keyword
- **AND** the response SHALL include related Keywords via shared Content

#### Scenario: Get graph by platform and keyword

- **WHEN** both `platform` and `keyword` parameters are provided
- **THEN** the response SHALL filter by both criteria

### Requirement: Media Keyword Search

The system SHALL provide keyword search functionality for media graph.

#### Scenario: Search keywords

- **WHEN** a GET request is made to `/api/v1/graph/media/search?q=游`
- **THEN** the response SHALL include Keywords matching the search query
- **AND** each result SHALL include the keyword name and content count

#### Scenario: Get popular keywords by platform

- **WHEN** a GET request is made to `/api/v1/graph/media/keywords?platform=bilibili`
- **THEN** the response SHALL include top keywords for the platform ordered by content count

#### Scenario: Get popular keywords across platforms

- **WHEN** a GET request is made to `/api/v1/graph/media/keywords` without platform filter
- **THEN** the response SHALL include top keywords across all platforms

### Requirement: Idempotent Sync Operations

The system SHALL perform idempotent sync operations to prevent data duplication.

#### Scenario: Re-sync existing content

- **WHEN** content that already exists in Neo4j is synced again
- **THEN** the existing node SHALL be updated (not duplicated)
- **AND** relationships SHALL be preserved or updated

#### Scenario: Sync failure recovery

- **WHEN** a sync operation fails partway through
- **THEN** a subsequent sync SHALL resume without duplicating already-synced data

### Requirement: Platform Support Configuration

The system SHALL support 7 platforms: Bilibili, Douyin, Kuaishou, Weibo, XHS (Xiaohongshu), Tieba, Zhihu.

#### Scenario: Bilibili sync

- **WHEN** syncing Bilibili data
- **THEN** `BilibiliVideo` records SHALL be synced as Content nodes with `contentType: "video"`
- **AND** `BilibiliVideoComment` records SHALL be synced as Comment nodes

#### Scenario: Douyin sync

- **WHEN** syncing Douyin data
- **THEN** `DouyinAweme` records SHALL be synced as Content nodes
- **AND** `DouyinAwemeComment` records SHALL be synced as Comment nodes

#### Scenario: Kuaishou sync

- **WHEN** syncing Kuaishou data
- **THEN** `KuaishouVideo` records SHALL be synced as Content nodes
- **AND** `KuaishouVideoComment` records SHALL be synced as Comment nodes

#### Scenario: Weibo sync

- **WHEN** syncing Weibo data
- **THEN** `WeiboNote` records SHALL be synced as Content nodes with `contentType: "note"`
- **AND** `WeiboNoteComment` records SHALL be synced as Comment nodes

#### Scenario: Tieba sync

- **WHEN** syncing Tieba data
- **THEN** `TiebaNote` records SHALL be synced as Content nodes with `contentType: "post"`
- **AND** `TiebaComment` records SHALL be synced as Comment nodes

#### Scenario: XHS sync

- **WHEN** syncing XHS (Xiaohongshu) data
- **THEN** `XhsNote` records SHALL be synced as Content nodes with `contentType: "note"`
- **AND** `XhsNoteComment` records SHALL be synced as Comment nodes
- **AND** `tag_list` field SHALL be parsed for keyword extraction

#### Scenario: Zhihu sync

- **WHEN** syncing Zhihu data
- **THEN** `ZhihuContent` records SHALL be synced as Content nodes
- **AND** `ZhihuComment` records SHALL be synced as Comment nodes

