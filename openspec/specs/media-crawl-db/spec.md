# media-crawl-db Specification

## Purpose
TBD - created by archiving change add-media-crawl-backend. Update Purpose after archive.
## Requirements
### Requirement: MySQL Database Configuration
The system SHALL support a separate external MySQL database for media crawl models alongside the existing PostgreSQL database.

#### Scenario: MySQL connection configured
- **WHEN** the application starts with `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE` environment variables set
- **THEN** Django SHALL connect to the external MySQL database as the `mysql` database alias

#### Scenario: MySQL connection unavailable
- **WHEN** the external MySQL server is unavailable and `MEDIA_CRAWL_ENABLED=True`
- **THEN** the system SHALL log a warning and media crawl endpoints SHALL return 503 Service Unavailable

### Requirement: Database Router
The system SHALL use a Django Database Router to route `media_crawl` app models to the MySQL database.

#### Scenario: Read operations routed to MySQL
- **WHEN** a read query is made on any model in the `media_crawl` app
- **THEN** the query SHALL be executed against the `mysql` database

#### Scenario: Write operations routed to MySQL
- **WHEN** a write query is made on any model in the `media_crawl` app
- **THEN** the query SHALL be executed against the `mysql` database

#### Scenario: Migrations routed correctly
- **WHEN** running `python manage.py migrate media_crawl --database=mysql`
- **THEN** the `media_crawl` app migrations SHALL be applied to the MySQL database only

#### Scenario: Other apps use default database
- **WHEN** a query is made on models from other apps (e.g., `crawl`, `graph`)
- **THEN** the query SHALL be executed against the `default` (PostgreSQL) database

### Requirement: Bilibili Models
The system SHALL provide Django ORM models for Bilibili platform data storage.

#### Scenario: BilibiliVideo model fields
- **WHEN** a `BilibiliVideo` record is created
- **THEN** it SHALL store: `video_id` (unique, indexed), `video_url`, `user_id`, `nickname`, `avatar`, `liked_count`, `add_ts`, `last_modify_ts`, `video_type`, `title`, `desc`, `create_time`, `disliked_count`, `video_play_count`, `video_favorite_count`, `video_share_count`, `video_coin_count`, `video_danmaku`, `video_comment`, `video_cover_url`, `source_keyword`

#### Scenario: BilibiliVideoComment model fields
- **WHEN** a `BilibiliVideoComment` record is created
- **THEN** it SHALL store: `user_id`, `nickname`, `sex`, `sign`, `avatar`, `add_ts`, `last_modify_ts`, `comment_id` (indexed), `video_id` (indexed), `content`, `create_time`, `sub_comment_count`, `parent_comment_id`, `like_count`

#### Scenario: BilibiliUpInfo model fields
- **WHEN** a `BilibiliUpInfo` record is created
- **THEN** it SHALL store: `user_id` (indexed), `nickname`, `sex`, `sign`, `avatar`, `add_ts`, `last_modify_ts`, `total_fans`, `total_liked`, `user_rank`, `is_official`

#### Scenario: BilibiliContactInfo model fields
- **WHEN** a `BilibiliContactInfo` record is created
- **THEN** it SHALL store: `up_id` (indexed), `fan_id` (indexed), `up_name`, `fan_name`, `up_sign`, `fan_sign`, `up_avatar`, `fan_avatar`, `add_ts`, `last_modify_ts`

#### Scenario: BilibiliUpDynamic model fields
- **WHEN** a `BilibiliUpDynamic` record is created
- **THEN** it SHALL store: `dynamic_id` (indexed), `user_id`, `user_name`, `text`, `type`, `pub_ts`, `total_comments`, `total_forwards`, `total_liked`, `add_ts`, `last_modify_ts`

### Requirement: Douyin Models
The system SHALL provide Django ORM models for Douyin platform data storage.

#### Scenario: DouyinAweme model fields
- **WHEN** a `DouyinAweme` record is created
- **THEN** it SHALL store: `user_id`, `sec_uid`, `short_user_id`, `user_unique_id`, `nickname`, `avatar`, `user_signature`, `ip_location`, `add_ts`, `last_modify_ts`, `aweme_id` (indexed), `aweme_type`, `title`, `desc`, `create_time` (indexed), `liked_count`, `comment_count`, `share_count`, `collected_count`, `aweme_url`, `cover_url`, `video_download_url`, `music_download_url`, `note_download_url`, `source_keyword`

#### Scenario: DouyinAwemeComment model fields
- **WHEN** a `DouyinAwemeComment` record is created
- **THEN** it SHALL store: `user_id`, `sec_uid`, `short_user_id`, `user_unique_id`, `nickname`, `avatar`, `user_signature`, `ip_location`, `add_ts`, `last_modify_ts`, `comment_id` (indexed), `aweme_id` (indexed), `content`, `create_time`, `sub_comment_count`, `parent_comment_id`, `like_count`, `pictures`

#### Scenario: DyCreator model fields
- **WHEN** a `DyCreator` record is created
- **THEN** it SHALL store: `user_id`, `nickname`, `avatar`, `ip_location`, `add_ts`, `last_modify_ts`, `desc`, `gender`, `follows`, `fans`, `interaction`, `videos_count`

### Requirement: Kuaishou Models
The system SHALL provide Django ORM models for Kuaishou platform data storage.

#### Scenario: KuaishouVideo model fields
- **WHEN** a `KuaishouVideo` record is created
- **THEN** it SHALL store: `user_id`, `nickname`, `avatar`, `add_ts`, `last_modify_ts`, `video_id` (indexed), `video_type`, `title`, `desc`, `create_time` (indexed), `liked_count`, `viewd_count`, `video_url`, `video_cover_url`, `video_play_url`, `source_keyword`

#### Scenario: KuaishouVideoComment model fields
- **WHEN** a `KuaishouVideoComment` record is created
- **THEN** it SHALL store: `user_id`, `nickname`, `avatar`, `add_ts`, `last_modify_ts`, `comment_id` (indexed), `video_id` (indexed), `content`, `create_time`, `sub_comment_count`

### Requirement: Weibo Models
The system SHALL provide Django ORM models for Weibo platform data storage.

#### Scenario: WeiboNote model fields
- **WHEN** a `WeiboNote` record is created
- **THEN** it SHALL store: `user_id`, `nickname`, `avatar`, `gender`, `profile_url`, `ip_location`, `add_ts`, `last_modify_ts`, `note_id` (indexed), `content`, `create_time` (indexed), `create_date_time` (indexed), `liked_count`, `comments_count`, `shared_count`, `note_url`, `source_keyword`

#### Scenario: WeiboNoteComment model fields
- **WHEN** a `WeiboNoteComment` record is created
- **THEN** it SHALL store: `user_id`, `nickname`, `avatar`, `gender`, `profile_url`, `ip_location`, `add_ts`, `last_modify_ts`, `comment_id` (indexed), `note_id` (indexed), `content`, `create_time`, `create_date_time` (indexed), `comment_like_count`, `sub_comment_count`, `parent_comment_id`

#### Scenario: WeiboCreator model fields
- **WHEN** a `WeiboCreator` record is created
- **THEN** it SHALL store: `user_id`, `nickname`, `avatar`, `ip_location`, `add_ts`, `last_modify_ts`, `desc`, `gender`, `follows`, `fans`, `tag_list`

### Requirement: Xiaohongshu Models
The system SHALL provide Django ORM models for Xiaohongshu (XHS) platform data storage.

#### Scenario: XhsCreator model fields
- **WHEN** a `XhsCreator` record is created
- **THEN** it SHALL store: `user_id`, `nickname`, `avatar`, `ip_location`, `add_ts`, `last_modify_ts`, `desc`, `gender`, `follows`, `fans`, `interaction`, `tag_list`

#### Scenario: XhsNote model fields
- **WHEN** a `XhsNote` record is created
- **THEN** it SHALL store: `user_id`, `nickname`, `avatar`, `ip_location`, `add_ts`, `last_modify_ts`, `note_id` (indexed), `type`, `title`, `desc`, `video_url`, `time` (indexed), `last_update_time`, `liked_count`, `collected_count`, `comment_count`, `share_count`, `image_list`, `tag_list`, `note_url`, `source_keyword`, `xsec_token`

#### Scenario: XhsNoteComment model fields
- **WHEN** a `XhsNoteComment` record is created
- **THEN** it SHALL store: `user_id`, `nickname`, `avatar`, `ip_location`, `add_ts`, `last_modify_ts`, `comment_id` (indexed), `create_time` (indexed), `note_id`, `content`, `sub_comment_count`, `pictures`, `parent_comment_id`, `like_count`

### Requirement: Tieba Models
The system SHALL provide Django ORM models for Tieba platform data storage.

#### Scenario: TiebaNote model fields
- **WHEN** a `TiebaNote` record is created
- **THEN** it SHALL store: `note_id` (indexed), `title`, `desc`, `note_url`, `publish_time` (indexed), `user_link`, `user_nickname`, `user_avatar`, `tieba_id`, `tieba_name`, `tieba_link`, `total_replay_num`, `total_replay_page`, `ip_location`, `add_ts`, `last_modify_ts`, `source_keyword`

#### Scenario: TiebaComment model fields
- **WHEN** a `TiebaComment` record is created
- **THEN** it SHALL store: `comment_id` (indexed), `parent_comment_id`, `content`, `user_link`, `user_nickname`, `user_avatar`, `tieba_id`, `tieba_name`, `tieba_link`, `publish_time` (indexed), `ip_location`, `sub_comment_count`, `note_id` (indexed), `note_url`, `add_ts`, `last_modify_ts`

#### Scenario: TiebaCreator model fields
- **WHEN** a `TiebaCreator` record is created
- **THEN** it SHALL store: `user_id`, `user_name`, `nickname`, `avatar`, `ip_location`, `add_ts`, `last_modify_ts`, `gender`, `follows`, `fans`, `registration_duration`

### Requirement: Zhihu Models
The system SHALL provide Django ORM models for Zhihu platform data storage.

#### Scenario: ZhihuContent model fields
- **WHEN** a `ZhihuContent` record is created
- **THEN** it SHALL store: `content_id` (indexed), `content_type`, `content_text`, `content_url`, `question_id`, `title`, `desc`, `created_time` (indexed), `updated_time`, `voteup_count`, `comment_count`, `source_keyword`, `user_id`, `user_link`, `user_nickname`, `user_avatar`, `user_url_token`, `add_ts`, `last_modify_ts`

#### Scenario: ZhihuComment model fields
- **WHEN** a `ZhihuComment` record is created
- **THEN** it SHALL store: `comment_id` (indexed), `parent_comment_id`, `content`, `publish_time` (indexed), `ip_location`, `sub_comment_count`, `like_count`, `dislike_count`, `content_id` (indexed), `content_type`, `user_id`, `user_link`, `user_nickname`, `user_avatar`, `add_ts`, `last_modify_ts`

#### Scenario: ZhihuCreator model fields
- **WHEN** a `ZhihuCreator` record is created
- **THEN** it SHALL store: `user_id` (unique, indexed), `user_link`, `user_nickname`, `user_avatar`, `url_token`, `gender`, `ip_location`, `follows`, `fans`, `anwser_count`, `video_count`, `question_count`, `article_count`, `column_count`, `get_voteup_count`, `add_ts`, `last_modify_ts`

### Requirement: Feature Toggle
The system SHALL provide configuration settings to enable/disable media crawl functionality.

#### Scenario: Media crawl disabled
- **WHEN** `MEDIA_CRAWL_ENABLED` is set to `False`
- **THEN** the media crawl API endpoints SHALL return 503 Service Unavailable

#### Scenario: Media crawl enabled
- **WHEN** `MEDIA_CRAWL_ENABLED` is set to `True`
- **THEN** the media crawl API endpoints SHALL be fully functional

#### Scenario: CrawlTask integration disabled
- **WHEN** `MEDIA_CRAWL_INTEGRATION_ENABLED` is set to `False`
- **THEN** CrawlTask SHALL NOT trigger media platform crawls

#### Scenario: CrawlTask integration enabled
- **WHEN** `MEDIA_CRAWL_INTEGRATION_ENABLED` is set to `True`
- **THEN** CrawlTask MAY trigger media platform crawls based on `media_platform` field

