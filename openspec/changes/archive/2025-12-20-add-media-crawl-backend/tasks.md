## 1. Infrastructure Setup

- [x] 1.1 Add MySQL environment variables to `.env.example` (external server connection)
- [x] 1.2 Add `mysqlclient` to `backend/requirements/base.txt`

## 2. Django Database Configuration

- [x] 2.1 Add MySQL database config in `backend/config/settings/base.py`
- [x] 2.2 Create `backend/apps/media_crawl/db_router.py` with `MediaCrawlRouter`
- [x] 2.3 Add `DATABASE_ROUTERS` setting

## 3. Create Media Crawl App

- [x] 3.1 Create `backend/apps/media_crawl/` directory structure
- [x] 3.2 Create `apps.py` with `MediaCrawlConfig`
- [x] 3.3 Add `media_crawl` to `INSTALLED_APPS`
- [x] 3.4 Add `MEDIA_CRAWL_ENABLED` and `MEDIA_CRAWL_INTEGRATION_ENABLED` settings

## 4. Django Models (Convert from SQLAlchemy)

- [x] 4.1 Create Bilibili models: `BilibiliVideo`, `BilibiliVideoComment`, `BilibiliUpInfo`, `BilibiliContactInfo`, `BilibiliUpDynamic`
- [x] 4.2 Create Douyin models: `DouyinAweme`, `DouyinAwemeComment`, `DyCreator`
- [x] 4.3 Create Kuaishou models: `KuaishouVideo`, `KuaishouVideoComment`
- [x] 4.4 Create Weibo models: `WeiboNote`, `WeiboNoteComment`, `WeiboCreator`
- [x] 4.5 Create Xiaohongshu models: `XhsCreator`, `XhsNote`, `XhsNoteComment`
- [x] 4.6 Create Tieba models: `TiebaNote`, `TiebaComment`, `TiebaCreator`
- [x] 4.7 Create Zhihu models: `ZhihuContent`, `ZhihuComment`, `ZhihuCreator`
- [x] 4.8 Create and run migrations: `python manage.py makemigrations media_crawl` and `python manage.py migrate media_crawl --database=mysql`

## 5. API Schemas

- [x] 5.1 Create base schemas in `backend/apps/media_crawl/schemas/base.py`
- [x] 5.2 Create Bilibili schemas in `backend/apps/media_crawl/schemas/bilibili.py`
- [x] 5.3 Create Douyin schemas in `backend/apps/media_crawl/schemas/douyin.py`
- [x] 5.4 Create Kuaishou schemas in `backend/apps/media_crawl/schemas/kuaishou.py`
- [x] 5.5 Create Weibo schemas in `backend/apps/media_crawl/schemas/weibo.py`
- [x] 5.6 Create Xiaohongshu schemas in `backend/apps/media_crawl/schemas/xhs.py`
- [x] 5.7 Create Tieba schemas in `backend/apps/media_crawl/schemas/tieba.py`
- [x] 5.8 Create Zhihu schemas in `backend/apps/media_crawl/schemas/zhihu.py`

## 6. API Endpoints

- [x] 6.1 Create base CRUD router factory in `backend/apps/media_crawl/api/base.py`
- [x] 6.2 Create Bilibili API in `backend/apps/media_crawl/api/bilibili.py`
- [x] 6.3 Create Douyin API in `backend/apps/media_crawl/api/douyin.py`
- [x] 6.4 Create Kuaishou API in `backend/apps/media_crawl/api/kuaishou.py`
- [x] 6.5 Create Weibo API in `backend/apps/media_crawl/api/weibo.py`
- [x] 6.6 Create Xiaohongshu API in `backend/apps/media_crawl/api/xhs.py`
- [x] 6.7 Create Tieba API in `backend/apps/media_crawl/api/tieba.py`
- [x] 6.8 Create Zhihu API in `backend/apps/media_crawl/api/zhihu.py`
- [x] 6.9 Create main router in `backend/apps/media_crawl/api/__init__.py`

## 7. URL Integration

- [x] 7.1 Update `backend/config/urls.py` to include media_crawl API router

## 8. CrawlTask Integration (Optional)

- [x] 8.1 Create integration service in `backend/services/media_crawl_integration.py`
- [x] 8.2 Add `media_platform` and `media_crawl_enabled` fields to `CrawlTask` model

## 9. Admin Interface

- [x] 9.1 Register all models in `backend/apps/media_crawl/admin.py`
