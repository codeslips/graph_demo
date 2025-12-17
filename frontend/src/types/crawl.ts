/**
 * Crawl task types for API interactions.
 */

export type TaskStatus = 'PENDING' | 'RUNNING' | 'DONE' | 'FAILED'
export type CrawlType = 'news_list' | 'article' | 'channel'

export interface CrawlTask {
  id: string
  target_url: string
  crawl_type: CrawlType
  status: TaskStatus
  total_items: number
  created_at: string
  started_at: string | null
  finished_at: string | null
  error_message: string
  celery_task_id?: string
}

export interface CreateTaskRequest {
  target_url: string
  crawl_type: CrawlType
}

export interface TaskListResponse {
  items: CrawlTask[]
  total: number
  page: number
  page_size: number
  has_next: boolean
}

export interface CrawlItem {
  id: string
  cont_id: string
  url: string
  title: string
  author: string
  summary: string
  channel_name: string
  publish_time: string | null
  tags: Array<{ tagId: number; tag: string }>
  neo4j_synced: boolean
  created_at: string
}

export interface ItemListResponse {
  items: CrawlItem[]
  total: number
  page: number
  page_size: number
}

