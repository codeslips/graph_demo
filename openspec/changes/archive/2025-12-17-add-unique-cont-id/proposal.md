# Change: Add Unique Constraint to CrawlItem.cont_id

## Why

Currently, the `cont_id` field in `CrawlItem` is not unique, allowing duplicate articles to be stored in the database. When crawling the same channel multiple times or overlapping content, duplicate records are created. Making `cont_id` unique ensures data integrity and prevents storage waste.

## What Changes

- **BREAKING**: Add `unique=True` constraint to `CrawlItem.cont_id` field
- Modify crawl logic to skip articles that already exist in the database (by `cont_id`)
- Add database migration to enforce uniqueness

## Impact

- Affected specs: `crawl-tasks`
- Affected code:
  - `backend/apps/crawl/models.py` - Add unique constraint
  - `backend/apps/crawl/tasks.py` - Add duplicate check before creating items
  - New migration file for schema change

