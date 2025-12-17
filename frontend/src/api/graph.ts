/**
 * Graph API functions.
 */

import request from './request'
import type { GraphData, KeywordListResponse, SearchResponse } from '@/types/graph'

/**
 * Get graph data for a specific task.
 */
export async function getTaskGraph(taskId: string): Promise<GraphData> {
  return request.get(`/graph/task/${taskId}`)
}

/**
 * Get popular keywords/tags.
 */
export async function getKeywords(params?: {
  limit?: number
  task_id?: string
}): Promise<KeywordListResponse> {
  return request.get('/graph/keywords', { params })
}

/**
 * Search graph nodes by text.
 */
export async function searchNodes(
  query: string,
  limit: number = 20
): Promise<SearchResponse> {
  return request.get('/graph/search', { params: { q: query, limit } })
}

