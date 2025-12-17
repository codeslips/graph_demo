# Project Context

## Purpose

**澎湃新闻 Web Crawl → Graph Insight Demo** (ThePaper Graph)

A complete system that implements:
1. **Configurable web crawling** from 澎湃新闻 (ThePaper.cn)
2. **Async task execution** via Celery for background processing
3. **Neo4j graph storage** for relationship-based data modeling
4. **Frontend visualization** with interactive graph exploration

### Core Goals
- Crawl news articles from 澎湃新闻 (ThePaper)
- Store data with relationships in Neo4j (articles, keywords, authors, channels)
- Provide interactive visualization on the frontend

## Tech Stack

### Backend
- **Framework**: Django 5.x + Django Ninja (API)
- **Database**: PostgreSQL 15+
- **Graph Database**: Neo4j 5.x
- **Task Queue**: Celery 5.x + Redis 7.x
- **Web Crawler**: httpx + BeautifulSoup4 + lxml

### Frontend
- **Framework**: Vue 3 + TypeScript
- **Build Tool**: Vite
- **Package Manager**: pnpm
- **Graph Visualization**: ECharts / Cytoscape.js
- **State Management**: Pinia

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (production)

## Project Conventions

### Code Style

#### Python (Backend)
- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Use `snake_case` for functions/variables, `PascalCase` for classes
- Django apps located in `backend/apps/`
- Business logic in `backend/services/`
- Crawler logic in `backend/crawler/`

#### TypeScript (Frontend)
- Use strict TypeScript with `tsconfig.json` strict mode
- Vue 3 Composition API with `<script setup>` syntax
- Composables in `src/composables/`
- API functions in `src/api/`
- Types defined in `src/types/`

#### Naming Conventions
- Files: `kebab-case` for components, `snake_case` for Python modules
- Components: `PascalCase` (e.g., `TaskCard.vue`)
- API endpoints: `kebab-case` (e.g., `/api/v1/crawl/tasks`)
- Database tables: `snake_case` with app prefix (e.g., `crawl_task`)

### Architecture Patterns

#### Backend
- **Django Apps**: Modular apps in `apps/` directory
  - `crawl/` - Crawl task management
  - `graph/` - Neo4j query interface
- **Service Layer**: Business logic in `services/` directory
  - `neo4j_client.py` - Neo4j connection management
  - `neo4j_sync.py` - Data sync to Neo4j
  - `crawl_service.py` - Crawl orchestration
- **Crawler Module**: Separate crawler package with base classes
  - `crawler/base.py` - Abstract crawler base
  - `crawler/thepaper/` - ThePaper-specific implementation

#### Frontend
- **Layout**: Shared layout components in `components/layout/`
- **Feature Components**: Organized by feature (`task/`, `graph/`)
- **API Layer**: Centralized API calls with axios instance
- **State**: Pinia stores for task and graph state

#### API Design
- RESTful API via Django Ninja
- Base URL: `/api/v1/`
- Endpoints:
  - `POST /api/v1/crawl/tasks` - Create crawl task
  - `GET /api/v1/crawl/tasks` - List tasks
  - `GET /api/v1/crawl/tasks/{id}` - Task details
  - `DELETE /api/v1/crawl/tasks/{id}` - Cancel/delete task
  - `GET /api/v1/graph/task/{id}` - Get graph data for task
  - `GET /api/v1/graph/keywords` - Hot keywords
  - `GET /api/v1/graph/search` - Search nodes

### Testing Strategy
- Backend: pytest with Django test client
- Test files colocated in `tests/` subdirectories within apps
- Focus on API endpoint testing and service layer testing
- No auto-generated tests unless explicitly requested

### Git Workflow
- Feature branches for new capabilities
- Commits should reference change IDs when applicable
- Keep commits atomic and focused

## Domain Context

### News Crawling Domain
- **CrawlTask**: Represents a single crawl job with status tracking
  - States: `PENDING` → `RUNNING` → `DONE` | `FAILED`
  - Types: `news_list`, `article`, `channel`
- **CrawlItem**: Individual crawled article metadata
  - Tracks sync status to Neo4j via `neo4j_synced` flag

### Graph Domain
- **Nodes**: 
  - `Website` - The news source (澎湃新闻)
  - `Channel` - News categories/sections
  - `Article` - Individual news articles
  - `Keyword` - Extracted keywords from articles
  - `Author` - Article authors
- **Relationships**:
  - `HAS_CHANNEL` - Website → Channel
  - `CONTAINS` - Channel → Article
  - `MENTIONS` - Article → Keyword (with weight)
  - `WRITTEN_BY` - Article → Author
  - `LINKS_TO` - Article → Article (cross-references)
  - `RELATED_TO` - Keyword → Keyword (with strength)

### Async Task Flow
1. API receives crawl request → Creates CrawlTask (PENDING)
2. Celery task starts → Updates to RUNNING
3. Crawler fetches pages → Parses articles → Extracts keywords
4. Results saved to PostgreSQL (CrawlItem)
5. Data synced to Neo4j (nodes + relationships)
6. Task marked DONE (or FAILED with error_message)

## Important Constraints

### Technical Constraints
- All async operations via Celery (no synchronous crawling in request cycle)
- Neo4j sync must be idempotent (safe to retry)
- Crawl rate limiting: configurable delay between requests (default 1.0s)
- Maximum retries: 3 per request
- Request timeout: 30 seconds

### Anti-Crawl Considerations
- Configurable User-Agent header
- Request delay between pages
- Retry logic with exponential backoff
- May need cookie/session handling (TBD)

### Data Integrity
- PostgreSQL as source of truth for task state
- Neo4j synced asynchronously after PostgreSQL write
- `neo4j_synced` flag tracks sync status per item

## External Dependencies

### Core Services
| Service    | Purpose                    | Port(s)      |
|------------|----------------------------|--------------|
| PostgreSQL | Primary database           | 5432         |
| Neo4j      | Graph database             | 7474, 7687   |
| Redis      | Celery broker/result store | 6379         |

### External APIs/Sites
| Site             | Purpose              | Notes                    |
|------------------|----------------------|--------------------------|
| thepaper.cn      | News source          | Crawl target             |

### Environment Variables (from `.env`)
```
# Django
SECRET_KEY, DEBUG, ALLOWED_HOSTS

# PostgreSQL
POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT

# Neo4j
NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

# Redis/Celery
REDIS_URL, CELERY_BROKER_URL, CELERY_RESULT_BACKEND

# Crawler
CRAWL_REQUEST_DELAY, CRAWL_MAX_RETRIES, CRAWL_TIMEOUT, CRAWL_USER_AGENT
```

## Pending Configuration (TBD)
- [ ] 澎湃新闻具体 URL 结构
- [ ] 目标爬取频道/栏目
- [ ] 页面选择器 (CSS / XPath)
- [ ] 是否需要登录/Cookie
- [ ] 爬取深度/数量限制
- [ ] 特殊反爬处理需求
