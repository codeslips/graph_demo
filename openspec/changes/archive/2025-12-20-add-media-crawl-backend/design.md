## Context

The system needs to store and manage crawled data from 7 social media platforms. The data is stored in a separate MySQL database while the existing ThePaper crawl system continues to use PostgreSQL.

Key stakeholders:
- Backend developers implementing CRUD operations
- Frontend developers consuming the API
- DevOps managing the dual-database infrastructure

## Goals / Non-Goals

### Goals
- Provide a unified Django app for all media platform models
- Support dual-database architecture (PostgreSQL + MySQL)
- Implement complete CRUD API for all 22 models
- Enable optional integration with existing CrawlTask system via feature switch

### Non-Goals
- Implementing actual crawl logic for each platform (future work)
- Data migration from existing sources
- Real-time sync between platforms
- Frontend UI for media crawl management

## Decisions

### 1. Single App vs Multiple Apps
**Decision**: Single unified `media_crawl` app
**Rationale**: 
- Models share similar structures (content, comment, creator patterns)
- Simpler DB router configuration (one app = one database)
- Easier maintenance with centralized schemas

**Alternatives considered**:
- Separate apps per platform: More isolation but increased complexity in routing and maintenance

### 2. Database Router Pattern
**Decision**: Class-based Django DB Router in `backend/apps/media_crawl/db_router.py`
**Rationale**:
- Django's recommended approach for multi-database setups
- Clean separation: all `media_crawl` models → `mysql`, others → `default` (PostgreSQL)

```python
class MediaCrawlRouter:
    app_label = 'media_crawl'
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'mysql'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'mysql'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations within same database only
        ...
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.app_label:
            return db == 'mysql'
        return db == 'default'
```

### 3. Model Naming Convention
**Decision**: Prefix models with platform name
**Pattern**: `{Platform}{EntityType}` (e.g., `BilibiliVideo`, `DouyinAweme`)
**Rationale**: Clear identification, consistent with source file, avoids naming conflicts

### 4. API Structure
**Decision**: Nested routers under `/api/v1/media/`
**Pattern**:
- `/api/v1/media/bilibili/videos/`
- `/api/v1/media/bilibili/comments/`
- `/api/v1/media/douyin/awemes/`
- etc.

**Rationale**: 
- Clear REST hierarchy
- Platform-scoped endpoints
- Consistent with existing `/api/v1/crawl/` and `/api/v1/graph/` patterns

### 5. Feature Toggle Integration
**Decision**: Add `MEDIA_CRAWL_INTEGRATION_ENABLED` setting
**Rationale**: 
- Allows gradual rollout
- Existing CrawlTask can optionally trigger media crawls
- Easy to enable/disable without code changes

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Cross-database queries fail | Document limitation; no FK relations across databases |
| External MySQL server unavailable | Graceful degradation with `MEDIA_CRAWL_ENABLED` toggle; proper error handling |
| MySQL connection pool exhaustion | Configure `CONN_MAX_AGE` and pool settings |
| Schema drift between SQLAlchemy source and Django models | Careful conversion; document field mapping |
| Large number of endpoints (22 models × 5 operations) | Use Django Ninja's class-based views for DRY implementation |

## Migration Plan

1. Configure MySQL connection settings in Django (external server via environment variables)
2. Add DB Router
3. Create Django models (convert from SQLAlchemy)
4. Run migrations against MySQL: `python manage.py migrate media_crawl --database=mysql`
5. Implement API endpoints
6. Add feature toggle for CrawlTask integration

**Rollback**: 
- Remove `media_crawl` from `INSTALLED_APPS`
- Remove MySQL database config from settings
- Remove router from `DATABASE_ROUTERS`

## Open Questions

- [ ] MySQL version preference (8.0+ recommended for JSON support)
- [ ] Connection pooling strategy (django-mysql-pool vs mysqlclient defaults)
- [ ] Batch operation limits for bulk CRUD endpoints

