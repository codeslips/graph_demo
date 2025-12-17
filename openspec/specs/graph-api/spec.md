# graph-api Specification

## Purpose
TBD - created by archiving change add-thepaper-crawl-system. Update Purpose after archive.
## Requirements
### Requirement: Task Graph Data API

The system SHALL provide an API endpoint to retrieve graph data for a specific crawl task.

#### Scenario: Get task graph data

- **WHEN** GET request to `/api/v1/graph/task/{task_id}`
- **THEN** response SHALL return nodes and edges for the task
- **AND** nodes SHALL include Article, Channel, and Tag entities
- **AND** edges SHALL include CONTAINS and HAS_TAG relationships
- **AND** response SHALL include stats (total nodes, edges, nodes by type)

#### Scenario: Task not found

- **WHEN** GET request with non-existent task_id
- **THEN** response SHALL return 404 with error message

#### Scenario: Empty graph

- **GIVEN** a task with no items synced to Neo4j
- **WHEN** GET request to graph endpoint
- **THEN** response SHALL return empty nodes and edges arrays
- **AND** stats SHALL show zero counts

### Requirement: Graph Response Format

The system SHALL return graph data in a format suitable for frontend visualization.

#### Scenario: Node structure

- **WHEN** graph data is returned
- **THEN** each node SHALL have `id`, `type`, `label`, and `properties` fields
- **AND** `id` SHALL be unique across all node types (e.g., `article_32169777`)
- **AND** `type` SHALL be one of: `Article`, `Channel`, `Tag`
- **AND** `label` SHALL be the display name (title, name, etc.)

#### Scenario: Edge structure

- **WHEN** graph data is returned
- **THEN** each edge SHALL have `source`, `target`, and `type` fields
- **AND** `source` and `target` SHALL reference node IDs
- **AND** `type` SHALL be the relationship type (CONTAINS, HAS_TAG)

### Requirement: Keywords API

The system SHALL provide an API endpoint to retrieve popular tags/keywords.

#### Scenario: Get popular keywords

- **WHEN** GET request to `/api/v1/graph/keywords`
- **THEN** response SHALL return tags ordered by article count
- **AND** each tag SHALL include `tagId`, `name`, and `count`
- **AND** results SHALL be limited to top 50 by default

#### Scenario: Filter by task

- **WHEN** GET request to `/api/v1/graph/keywords?task_id={id}`
- **THEN** results SHALL be filtered to tags from that task only

### Requirement: Node Search API

The system SHALL provide an API endpoint to search nodes by text.

#### Scenario: Search nodes by keyword

- **WHEN** GET request to `/api/v1/graph/search?q={query}`
- **THEN** response SHALL return nodes matching the query
- **AND** search SHALL match against Article titles and Tag names
- **AND** results SHALL be limited to 20 items

#### Scenario: Empty search results

- **WHEN** search query matches no nodes
- **THEN** response SHALL return empty array
- **AND** response status SHALL be 200

