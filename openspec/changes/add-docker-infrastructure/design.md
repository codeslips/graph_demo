## Context

This is a greenfield project that needs Docker infrastructure to orchestrate multiple services. The goal is to create a minimal, working skeleton that developers can start and build upon.

**Stakeholders**: Developers working on the ThePaper Graph project

**Constraints**:
- Must use the tech stack defined in `project.md`
- No business logic implementation - only structural scaffolding
- Development-first focus (production hardening comes later)

## Goals / Non-Goals

**Goals**:
- Single command to start all services (`docker compose up`)
- Hot-reload for both backend and frontend in development
- Services can communicate with each other
- Database migrations run on startup
- Health checks for service readiness

**Non-Goals**:
- Production deployment configuration
- SSL/TLS setup
- Business logic implementation
- CI/CD pipelines
- Monitoring/logging infrastructure

## Decisions

### Decision 1: Service Architecture
Use Docker Compose with the following services:
- `backend` - Django + Gunicorn (dev: Django runserver with hot-reload)
- `celery` - Celery worker
- `redis` - Message broker + result backend
- `postgres` - Primary database
- `neo4j` - Graph database
- `frontend` - Vue dev server (Vite)

**Rationale**: Matches the architecture defined in project specification. Each service isolated in its own container.

### Decision 2: Development vs Production Split
- `docker-compose.yml` - Base configuration
- `docker-compose.dev.yml` - Development overrides (volume mounts, hot-reload)

**Rationale**: Allows same base config for both environments with targeted overrides.

### Decision 3: Minimal Django Skeleton
Create only the structural files needed to boot:
- `config/` - Settings, URLs, WSGI/ASGI, Celery
- `apps/crawl/` - Empty app with models.py stub
- `apps/graph/` - Empty app with models.py stub
- `requirements/` - Dependency files

**Rationale**: Provides the structure from project spec without implementing logic.

### Decision 4: Minimal Vue Skeleton
Create Vite + Vue 3 + TypeScript project with:
- Basic `App.vue` with router outlet
- Empty route configuration
- API request utility stub

**Rationale**: Standard Vue 3 project structure matching project spec.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Services may fail to connect on first start | Add wait-for-it script and health checks |
| Neo4j cold start is slow | Document expected startup time |
| Version drift between dev and prod configs | Keep base config in main file, only overrides in dev |

## Migration Plan

Not applicable - greenfield project.

## Open Questions

None - scope is well-defined as minimal scaffold.

