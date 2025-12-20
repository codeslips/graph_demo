/**
 * Media Graph API functions.
 */

import request from './request'
import type {
  MediaGraphData,
  MediaKeywordListResponse,
  MediaSearchResponse,
  SyncNeo4jRequest,
  SyncNeo4jResponse,
  SyncStatusResponse,
} from '@/types/mediaGraph'

/**
 * Get media graph data.
 */
export async function getMediaGraph(params?: {
  platform?: string
  keyword?: string
  limit?: number
}): Promise<MediaGraphData> {
  return request.get('/graph/media', { params })
}

/**
 * Get popular media keywords.
 */
export async function getMediaKeywords(params?: {
  platform?: string
  limit?: number
}): Promise<MediaKeywordListResponse> {
  return request.get('/graph/media/keywords', { params })
}

/**
 * Search media graph keywords.
 */
export async function searchMediaKeywords(
  query: string,
  limit: number = 20
): Promise<MediaSearchResponse> {
  return request.get('/graph/media/search', { params: { q: query, limit } })
}

/**
 * Trigger Neo4j sync for media data.
 * @param payload - Optional sync configuration
 * @param syncMode - If true, run synchronously (blocking but immediate)
 */
export async function triggerMediaSync(
  payload?: SyncNeo4jRequest,
  syncMode: boolean = true  // Default to sync mode for reliable execution
): Promise<SyncNeo4jResponse> {
  return request.post('/media/sync-neo4j', { ...payload, sync: syncMode })
}

/**
 * Get media Neo4j sync status.
 */
export async function getMediaSyncStatus(): Promise<SyncStatusResponse> {
  return request.get('/media/sync-status')
}

