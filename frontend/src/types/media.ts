/**
 * Media Crawl TypeScript type definitions
 * Maps to backend/apps/media_crawl/models and schemas
 */

// ============== Common Types ==============

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  limit: number
  offset: number
}

export interface ErrorResponse {
  detail: string
  code?: string
}

export interface BatchDeleteRequest {
  ids: number[]
}

export interface BatchDeleteResponse {
  deleted_count: number
}

export interface FilterParams {
  user_id?: string
  create_time_from?: number
  create_time_to?: number
  source_keyword?: string
  limit?: number
  offset?: number
}

// ============== Platform Definitions ==============

export type Platform = 'bilibili' | 'douyin' | 'kuaishou' | 'weibo' | 'xhs' | 'tieba' | 'zhihu'

export interface PlatformConfig {
  id: Platform
  name: string
  icon: string
  entities: EntityConfig[]
}

export interface EntityConfig {
  id: string
  name: string
  apiPath: string
  columns: ColumnConfig[]
  primaryField?: string
}

export interface ColumnConfig {
  key: string
  label: string
  width?: number
  sortable?: boolean
  type?: 'text' | 'number' | 'date' | 'link' | 'image'
}

// ============== Bilibili Models ==============

export interface BilibiliVideo {
  id: number
  video_id: number
  video_url: string
  user_id?: number
  nickname?: string
  avatar?: string
  liked_count?: number
  video_type?: string
  title?: string
  desc?: string
  create_time?: number
  disliked_count?: string
  video_play_count?: string
  video_favorite_count?: string
  video_share_count?: string
  video_coin_count?: string
  video_danmaku?: string
  video_comment?: string
  video_cover_url?: string
  source_keyword?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface BilibiliVideoComment {
  id: number
  user_id?: string
  nickname?: string
  sex?: string
  sign?: string
  avatar?: string
  comment_id: number
  video_id: number
  content?: string
  create_time?: number
  sub_comment_count?: string
  parent_comment_id?: string
  like_count?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface BilibiliUpInfo {
  id: number
  user_id: number
  nickname?: string
  sex?: string
  sign?: string
  avatar?: string
  total_fans?: number
  total_liked?: number
  user_rank?: number
  is_official?: number
  add_ts?: number
  last_modify_ts?: number
}

export interface BilibiliContactInfo {
  id: number
  up_id: number
  fan_id: number
  up_name?: string
  fan_name?: string
  up_sign?: string
  fan_sign?: string
  up_avatar?: string
  fan_avatar?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface BilibiliUpDynamic {
  id: number
  dynamic_id: number
  user_id?: string
  user_name?: string
  text?: string
  type?: string
  pub_ts?: number
  total_comments?: number
  total_forwards?: number
  total_liked?: number
  add_ts?: number
  last_modify_ts?: number
}

// ============== Douyin Models ==============

export interface DouyinAweme {
  id: number
  user_id?: string
  sec_uid?: string
  short_user_id?: string
  user_unique_id?: string
  nickname?: string
  avatar?: string
  user_signature?: string
  ip_location?: string
  aweme_id: number
  aweme_type?: string
  title?: string
  desc?: string
  create_time?: number
  liked_count?: string
  comment_count?: string
  share_count?: string
  collected_count?: string
  aweme_url?: string
  cover_url?: string
  video_download_url?: string
  music_download_url?: string
  note_download_url?: string
  source_keyword?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface DouyinAwemeComment {
  id: number
  user_id?: string
  sec_uid?: string
  short_user_id?: string
  user_unique_id?: string
  nickname?: string
  avatar?: string
  user_signature?: string
  ip_location?: string
  comment_id: number
  aweme_id: number
  content?: string
  create_time?: number
  sub_comment_count?: string
  parent_comment_id?: string
  like_count?: string
  pictures?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface DyCreator {
  id: number
  user_id?: string
  nickname?: string
  avatar?: string
  ip_location?: string
  desc?: string
  gender?: string
  follows?: string
  fans?: string
  interaction?: string
  videos_count?: string
  add_ts?: number
  last_modify_ts?: number
}

// ============== Kuaishou Models ==============

export interface KuaishouVideo {
  id: number
  user_id?: string
  nickname?: string
  avatar?: string
  video_id: string
  video_type?: string
  title?: string
  desc?: string
  create_time?: number
  liked_count?: string
  viewd_count?: string
  video_url?: string
  video_cover_url?: string
  video_play_url?: string
  source_keyword?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface KuaishouVideoComment {
  id: number
  user_id?: string
  nickname?: string
  avatar?: string
  comment_id: number
  video_id: string
  content?: string
  create_time?: number
  sub_comment_count?: string
  add_ts?: number
  last_modify_ts?: number
}

// ============== Weibo Models ==============

export interface WeiboNote {
  id: number
  user_id?: string
  nickname?: string
  avatar?: string
  gender?: string
  profile_url?: string
  ip_location?: string
  note_id: number
  content?: string
  create_time?: number
  create_date_time?: string
  liked_count?: string
  comments_count?: string
  shared_count?: string
  note_url?: string
  source_keyword?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface WeiboNoteComment {
  id: number
  user_id?: string
  nickname?: string
  avatar?: string
  gender?: string
  profile_url?: string
  ip_location?: string
  comment_id: number
  note_id: number
  content?: string
  create_time?: number
  create_date_time?: string
  comment_like_count?: string
  sub_comment_count?: string
  parent_comment_id?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface WeiboCreator {
  id: number
  user_id?: string
  nickname?: string
  avatar?: string
  ip_location?: string
  desc?: string
  gender?: string
  follows?: string
  fans?: string
  tag_list?: string
  add_ts?: number
  last_modify_ts?: number
}

// ============== XHS (Xiaohongshu) Models ==============

export interface XhsCreator {
  id: number
  user_id?: string
  nickname?: string
  avatar?: string
  ip_location?: string
  desc?: string
  gender?: string
  follows?: string
  fans?: string
  interaction?: string
  tag_list?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface XhsNote {
  id: number
  user_id?: string
  nickname?: string
  avatar?: string
  ip_location?: string
  note_id: string
  type?: string
  title?: string
  desc?: string
  video_url?: string
  time?: number
  last_update_time?: number
  liked_count?: string
  collected_count?: string
  comment_count?: string
  share_count?: string
  image_list?: string
  tag_list?: string
  note_url?: string
  source_keyword?: string
  xsec_token?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface XhsNoteComment {
  id: number
  user_id?: string
  nickname?: string
  avatar?: string
  ip_location?: string
  comment_id: string
  create_time?: number
  note_id?: string
  content?: string
  sub_comment_count?: number
  pictures?: string
  parent_comment_id?: string
  like_count?: string
  add_ts?: number
  last_modify_ts?: number
}

// ============== Tieba Models ==============

export interface TiebaNote {
  id: number
  note_id: string
  title?: string
  desc?: string
  note_url?: string
  publish_time?: string
  user_link?: string
  user_nickname?: string
  user_avatar?: string
  tieba_id?: string
  tieba_name?: string
  tieba_link?: string
  total_replay_num?: number
  total_replay_page?: number
  ip_location?: string
  source_keyword?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface TiebaComment {
  id: number
  comment_id: string
  parent_comment_id?: string
  content?: string
  user_link?: string
  user_nickname?: string
  user_avatar?: string
  tieba_id?: string
  tieba_name?: string
  tieba_link?: string
  publish_time?: string
  ip_location?: string
  sub_comment_count?: number
  note_id: string
  note_url?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface TiebaCreator {
  id: number
  user_id?: string
  user_name?: string
  nickname?: string
  avatar?: string
  ip_location?: string
  gender?: string
  follows?: string
  fans?: string
  registration_duration?: string
  add_ts?: number
  last_modify_ts?: number
}

// ============== Zhihu Models ==============

export interface ZhihuContent {
  id: number
  content_id: string
  content_type?: string
  content_text?: string
  content_url?: string
  question_id?: string
  title?: string
  desc?: string
  created_time?: string
  updated_time?: string
  voteup_count?: number
  comment_count?: number
  source_keyword?: string
  user_id?: string
  user_link?: string
  user_nickname?: string
  user_avatar?: string
  user_url_token?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface ZhihuComment {
  id: number
  comment_id: string
  parent_comment_id?: string
  content?: string
  publish_time?: string
  ip_location?: string
  sub_comment_count?: number
  like_count?: number
  dislike_count?: number
  content_id: string
  content_type?: string
  user_id?: string
  user_link?: string
  user_nickname?: string
  user_avatar?: string
  add_ts?: number
  last_modify_ts?: number
}

export interface ZhihuCreator {
  id: number
  user_id: string
  user_link?: string
  user_nickname?: string
  user_avatar?: string
  url_token?: string
  gender?: string
  ip_location?: string
  follows?: number
  fans?: number
  anwser_count?: number
  video_count?: number
  question_count?: number
  article_count?: number
  column_count?: number
  get_voteup_count?: number
  add_ts?: number
  last_modify_ts?: number
}

// ============== Union Types for Generic Handling ==============

export type MediaRecord =
  | BilibiliVideo
  | BilibiliVideoComment
  | BilibiliUpInfo
  | BilibiliContactInfo
  | BilibiliUpDynamic
  | DouyinAweme
  | DouyinAwemeComment
  | DyCreator
  | KuaishouVideo
  | KuaishouVideoComment
  | WeiboNote
  | WeiboNoteComment
  | WeiboCreator
  | XhsCreator
  | XhsNote
  | XhsNoteComment
  | TiebaNote
  | TiebaComment
  | TiebaCreator
  | ZhihuContent
  | ZhihuComment
  | ZhihuCreator

// ============== API Status ==============

export interface MediaApiStatus {
  enabled: boolean
  integration_enabled: boolean
  platforms: Platform[]
}

