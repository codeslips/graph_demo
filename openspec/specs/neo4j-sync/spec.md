# neo4j-sync Specification

## Purpose
TBD - created by archiving change add-thepaper-crawl-system. Update Purpose after archive.
## Requirements
### Requirement: Neo4j Client Connection

The system SHALL provide a Neo4j client service for database operations.

#### Scenario: Connect to Neo4j

- **GIVEN** valid Neo4j credentials in environment variables
- **WHEN** the client is initialized
- **THEN** it SHALL establish a connection to the Neo4j database
- **AND** connection errors SHALL be logged and raised

#### Scenario: Connection pooling

- **GIVEN** multiple concurrent requests
- **WHEN** the Neo4j client is used
- **THEN** connections SHALL be pooled for efficiency
- **AND** connections SHALL be properly closed on shutdown

### Requirement: Graph Node Creation

The system SHALL create graph nodes for crawled entities.

#### Scenario: Create Website node

- **WHEN** syncing data for the first time
- **THEN** a Website node SHALL be created with `domain=thepaper.cn`
- **AND** subsequent syncs SHALL merge (not duplicate) the Website node

#### Scenario: Create Channel node

- **WHEN** an article with channel info is synced
- **THEN** a Channel node SHALL be created with `nodeId`, `name`, `desc`
- **AND** duplicate channels SHALL be merged by `nodeId`
- **AND** a `HAS_CHANNEL` relationship SHALL link Website to Channel

#### Scenario: Create Article node

- **WHEN** an article is synced
- **THEN** an Article node SHALL be created with `contId`, `title`, `author`, `pubTime`, `url`, `summary`
- **AND** a `CONTAINS` relationship SHALL link Channel to Article

#### Scenario: Create Tag node

- **WHEN** an article with tags is synced
- **THEN** Tag nodes SHALL be created for each tag with `tagId`, `name`
- **AND** duplicate tags SHALL be merged by `tagId`
- **AND** `HAS_TAG` relationships SHALL link Article to each Tag

### Requirement: Batch Sync After Crawl

The system SHALL sync all crawled items to Neo4j in batch after crawl completion.

#### Scenario: Batch sync success

- **GIVEN** a CrawlTask with multiple CrawlItems
- **WHEN** the crawl completes successfully
- **THEN** all items SHALL be synced to Neo4j in a single transaction batch
- **AND** `neo4j_synced` flag SHALL be set to `True` for each item

#### Scenario: Sync failure handling

- **GIVEN** a Neo4j sync operation fails
- **WHEN** the error is caught
- **THEN** the `neo4j_synced` flag SHALL remain `False`
- **AND** the task status SHALL still be set to `DONE` (items saved in PostgreSQL)
- **AND** the error SHALL be logged for debugging

