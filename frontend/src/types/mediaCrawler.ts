/**
 * TypeScript types for Media Crawler Task functionality
 */

// Supported platforms
export type CrawlerPlatform =
  | 'xhs'
  | 'douyin'
  | 'bilibili'
  | 'kuaishou'
  | 'weibo'
  | 'tieba'
  | 'zhihu'

// Login types
export type LoginType = 'qrcode' | 'cookie'

// Crawler types
export type CrawlerType = 'search' | 'detail' | 'creator'

/**
 * Request payload for starting a crawler task
 */
export interface CrawlerStartRequest {
  platform: CrawlerPlatform
  login_type: LoginType
  crawler_type: CrawlerType
  keywords?: string
  specified_ids?: string
  creator_ids?: string
  start_page?: number
  enable_comments?: boolean
  enable_sub_comments?: boolean
  save_option?: string
  cookies?: string
  headless?: boolean
}

/**
 * Response from starting a crawler task
 */
export interface CrawlerStartResponse {
  success: boolean
  message: string
}

/**
 * Crawler task status response
 */
export interface CrawlerStatusResponse {
  status: 'running' | 'idle'
  platform?: string
  crawler_type?: string
  started_at?: string
  error_message?: string
}

/**
 * Error response from crawler endpoints
 */
export interface CrawlerErrorResponse {
  detail: string
  code: string
}

/**
 * Platform option for dropdown
 */
export interface PlatformOption {
  value: CrawlerPlatform
  label: string
  icon: string
}

/**
 * Crawler type option for dropdown
 */
export interface CrawlerTypeOption {
  value: CrawlerType
  label: string
}

/**
 * Login type option for dropdown
 */
export interface LoginTypeOption {
  value: LoginType
  label: string
}

