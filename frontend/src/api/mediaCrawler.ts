/**
 * Media Crawler API functions
 * Provides operations to start and monitor crawler tasks
 */

import request from './request'
import type {
  CrawlerStartRequest,
  CrawlerStartResponse,
  CrawlerStatusResponse,
} from '@/types/mediaCrawler'

const CRAWLER_BASE_URL = '/media/crawler'

/**
 * Start a new crawler task
 */
export async function startCrawlerTask(
  payload: CrawlerStartRequest
): Promise<CrawlerStartResponse> {
  return request.post(`${CRAWLER_BASE_URL}/start`, payload)
}

/**
 * Get current crawler task status
 */
export async function getCrawlerStatus(): Promise<CrawlerStatusResponse> {
  return request.get(`${CRAWLER_BASE_URL}/status`)
}

