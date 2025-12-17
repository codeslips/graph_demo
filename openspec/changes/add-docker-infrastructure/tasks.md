## 1. Project Root Configuration

- [x] 1.1 Create `.env.example` with all environment variables
- [x] 1.2 Create `.gitignore` for Python, Node, Docker artifacts
- [x] 1.3 Create `Makefile` with common commands (up, down, logs, shell, migrate)

## 2. Docker Compose Setup

- [x] 2.1 Create `docker-compose.yml` with all services (postgres, redis, neo4j, backend, celery, frontend)
- [x] 2.2 Create `docker-compose.dev.yml` with development overrides (volumes, hot-reload)

## 3. Backend Skeleton (Django)

- [x] 3.1 Create `backend/Dockerfile` and `backend/Dockerfile.dev`
- [x] 3.2 Create `backend/requirements/` (base.txt, dev.txt, prod.txt)
- [x] 3.3 Create `backend/pyproject.toml`
- [x] 3.4 Create `backend/manage.py`
- [x] 3.5 Create `backend/config/` (settings, urls, wsgi, asgi, celery)
- [x] 3.6 Create `backend/apps/crawl/` skeleton (models, apps, admin, migrations)
- [x] 3.7 Create `backend/apps/graph/` skeleton (models, apps, admin, migrations)
- [x] 3.8 Create `backend/core/` utilities (empty stubs)
- [x] 3.9 Create `backend/services/` stubs (neo4j_client, crawl_service)
- [x] 3.10 Create `backend/crawler/` base structure

## 4. Frontend Skeleton (Vue 3)

- [x] 4.1 Create `frontend/Dockerfile` and `frontend/Dockerfile.dev`
- [x] 4.2 Create `frontend/package.json` with dependencies
- [x] 4.3 Create `frontend/vite.config.ts` and TypeScript configs
- [x] 4.4 Create `frontend/index.html` and `frontend/src/main.ts`
- [x] 4.5 Create `frontend/src/App.vue` with router outlet
- [x] 4.6 Create `frontend/src/router/index.ts` with placeholder routes
- [x] 4.7 Create `frontend/src/api/request.ts` axios instance

## 5. Scripts

- [x] 5.1 Create `scripts/wait_for_it.sh` for service dependencies
- [x] 5.2 Create `scripts/entrypoint.sh` for backend container

## 6. Validation

- [x] 6.1 Verify `docker compose config` validates successfully
- [x] 6.2 Verify `docker compose -f docker-compose.yml -f docker-compose.dev.yml config` validates
- [ ] 6.3 Verify backend responds on http://localhost:8000 (requires `make up`)
- [ ] 6.4 Verify frontend responds on http://localhost:5173 (requires `make up`)
- [ ] 6.5 Verify Neo4j browser accessible on http://localhost:7474 (requires `make up`)
