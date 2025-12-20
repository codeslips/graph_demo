# Change: Add Media Crawl Backend with MySQL Support

## Why

The project needs to manage crawled data from multiple social media platforms (Bilibili, Douyin, Kuaishou, Weibo, Xiaohongshu, Tieba, Zhihu). These models require a separate MySQL database with a DB router, while keeping existing ThePaper crawl system on PostgreSQL.

## What Changes

- Add new Django app `apps/media_crawl/` with unified models for all 7 platforms
- Add MySQL database configuration (external server) alongside existing PostgreSQL
- Add Django Database Router to route `media_crawl` models to MySQL
- Convert SQLAlchemy models from `media_crawl_model.py` to Django ORM
- Add Django Ninja API endpoints with full CRUD for all models:
  - Bilibili: Video, VideoComment, UpInfo, ContactInfo, UpDynamic
  - Douyin: Aweme, AwemeComment, Creator
  - Kuaishou: Video, VideoComment
  - Weibo: Note, NoteComment, Creator
  - Xiaohongshu: Creator, Note, NoteComment
  - Tieba: Note, Comment, Creator
  - Zhihu: Content, Comment, Creator
- Add integration switch to link with existing CrawlTask system (optional, disabled by default)
- Add `MEDIA_CRAWL_ENABLED` setting to enable/disable the media crawl feature

## Impact

- Affected specs: New `media-crawl-api`, `media-crawl-db` capabilities
- Affected code:
  - `backend/apps/media_crawl/` (new app)
  - `backend/config/settings/base.py` (database config, installed apps)
  - `backend/config/urls.py` (new API router)
  - `.env.example` (MySQL credentials for external server)

