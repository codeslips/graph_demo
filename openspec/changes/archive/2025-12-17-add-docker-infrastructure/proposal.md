# Change: Add Docker Infrastructure for Development

## Why

The project currently has only specification documents. To make the system runnable, we need to scaffold the basic Docker infrastructure that allows developers to start all services (Django, Celery, PostgreSQL, Neo4j, Redis, Vue frontend) with a single `docker compose up` command.

This change creates the minimal skeleton required to boot the system without implementing any business logic.

## What Changes

- Add `docker-compose.yml` with all required services
- Add `docker-compose.dev.yml` for development overrides
- Add `.env.example` with all environment variables
- Create minimal Django project skeleton (config + empty apps)
- Create minimal Vue 3 + Vite project skeleton
- Add Dockerfiles for backend and frontend
- Add initialization scripts
- Add `Makefile` for common commands

## Impact

- Affected specs: `docker-infrastructure` (new capability)
- Affected code: Creates entire project structure from scratch
- No breaking changes (greenfield project)

