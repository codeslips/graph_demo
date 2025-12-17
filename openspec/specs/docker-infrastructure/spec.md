# docker-infrastructure Specification

## Purpose
TBD - created by archiving change add-docker-infrastructure. Update Purpose after archive.
## Requirements
### Requirement: Docker Compose Orchestration

The system SHALL provide Docker Compose configuration that orchestrates all required services for the ThePaper Graph application.

#### Scenario: Start all services

- **GIVEN** a fresh clone of the repository
- **WHEN** the developer runs `docker compose up`
- **THEN** all services (postgres, redis, neo4j, backend, celery, frontend) SHALL start
- **AND** services SHALL wait for their dependencies before starting

#### Scenario: Development hot-reload

- **GIVEN** the development compose configuration is used
- **WHEN** the developer modifies backend Python files
- **THEN** the Django development server SHALL reload automatically
- **AND** when frontend TypeScript/Vue files are modified, Vite SHALL hot-reload

### Requirement: Service Connectivity

The system SHALL ensure all services can communicate with each other within the Docker network.

#### Scenario: Backend connects to databases

- **GIVEN** all services are running
- **WHEN** the backend service starts
- **THEN** it SHALL connect to PostgreSQL on `postgres:5432`
- **AND** it SHALL connect to Redis on `redis:6379`
- **AND** it SHALL connect to Neo4j on `neo4j:7687`

#### Scenario: Celery connects to broker

- **GIVEN** all services are running
- **WHEN** the Celery worker starts
- **THEN** it SHALL connect to Redis as the message broker
- **AND** it SHALL use Redis as the result backend

### Requirement: Environment Configuration

The system SHALL use environment variables for all configurable settings.

#### Scenario: Environment template provided

- **GIVEN** a developer clones the repository
- **WHEN** they examine the project root
- **THEN** they SHALL find `.env.example` with all required variables documented
- **AND** copying it to `.env` SHALL provide working defaults for development

### Requirement: Development Ports

The system SHALL expose services on predictable local ports for development.

#### Scenario: Access development services

- **GIVEN** all services are running in development mode
- **THEN** the Django backend SHALL be accessible on `http://localhost:8000`
- **AND** the Vue frontend SHALL be accessible on `http://localhost:5173`
- **AND** the Neo4j browser SHALL be accessible on `http://localhost:7474`
- **AND** PostgreSQL SHALL be accessible on `localhost:5432`

### Requirement: Minimal Backend Skeleton

The system SHALL provide a minimal Django project structure that boots successfully without business logic.

#### Scenario: Django starts without errors

- **GIVEN** the backend container starts
- **WHEN** Django loads the application
- **THEN** it SHALL complete startup without import errors
- **AND** it SHALL respond to HTTP requests on the configured port

### Requirement: Minimal Frontend Skeleton

The system SHALL provide a minimal Vue 3 + Vite project structure that boots successfully.

#### Scenario: Vite dev server starts

- **GIVEN** the frontend container starts
- **WHEN** Vite loads the application
- **THEN** it SHALL complete startup without errors
- **AND** it SHALL serve the application on the configured port

