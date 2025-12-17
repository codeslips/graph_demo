## 1. Database Schema

- [x] 1.1 Add `unique=True` to `CrawlItem.cont_id` field in `models.py`
- [x] 1.2 Generate database migration

## 2. Crawl Logic

- [x] 2.1 Add helper function to check if `cont_id` exists in database
- [x] 2.2 Modify `_execute_crawl` to skip existing articles before fetching detail
- [x] 2.3 Update logging to indicate skipped duplicates

## 3. Validation

- [x] 3.1 Verify migration applies correctly
- [x] 3.2 Test that duplicate `cont_id` raises IntegrityError
- [x] 3.3 Test that crawl skips existing articles

