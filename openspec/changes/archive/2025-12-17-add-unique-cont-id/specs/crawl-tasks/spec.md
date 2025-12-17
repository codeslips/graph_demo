## MODIFIED Requirements

### Requirement: Crawl Item Model

The system SHALL provide a `CrawlItem` model to store individual crawled articles.

#### Scenario: Store crawled article

- **WHEN** an article is successfully parsed
- **THEN** a `CrawlItem` record SHALL be created
- **AND** it SHALL store `title`, `url`, `author`, `publish_time`, `summary`, `category`
- **AND** it SHALL have a foreign key to the parent `CrawlTask`
- **AND** `neo4j_synced` flag SHALL be `False` initially

#### Scenario: Unique content ID constraint

- **GIVEN** the `cont_id` field identifies ThePaper article uniquely
- **WHEN** a CrawlItem is created
- **THEN** the `cont_id` field SHALL be unique across all CrawlItem records
- **WHEN** attempting to create a CrawlItem with a `cont_id` that already exists
- **THEN** the database SHALL reject the insert with an IntegrityError

## ADDED Requirements

### Requirement: Duplicate Article Detection

The system SHALL detect and skip duplicate articles during crawl execution.

#### Scenario: Skip existing articles during crawl

- **GIVEN** a crawl task is executing
- **AND** the article list contains an article with `cont_id` that already exists in the database
- **WHEN** the crawler processes that article
- **THEN** the crawler SHALL skip fetching the article detail
- **AND** the crawler SHALL NOT create a duplicate CrawlItem record
- **AND** the crawler SHALL log that the article was skipped as duplicate
- **AND** the skipped article SHALL NOT count toward `items_crawled` total

