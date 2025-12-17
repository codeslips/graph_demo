/**
 * Crawl task API functions.
 */

import request from './request'
import type {
  CrawlTask,
  CreateTaskRequest,
  TaskListResponse,
  ItemListResponse
} from '@/types/crawl'

/**
 * Create a new crawl task.
 */
export async function createTask(data: CreateTaskRequest): Promise<CrawlTask> {
  return request.post('/crawl/tasks', data)
}

/**
 * Get paginated list of crawl tasks.
 */
export async function listTasks(params?: {
  page?: number
  page_size?: number
  status?: string
}): Promise<TaskListResponse> {
  return request.get('/crawl/tasks', { params })
}

/**
 * Get a single task by ID.
 */
export async function getTask(taskId: string): Promise<CrawlTask> {
  return request.get(`/crawl/tasks/${taskId}`)
}

/**
 * Delete a task.
 */
export async function deleteTask(taskId: string): Promise<void> {
  return request.delete(`/crawl/tasks/${taskId}`)
}

/**
 * Get items for a task.
 */
export async function getTaskItems(
  taskId: string,
  params?: { page?: number; page_size?: number }
): Promise<ItemListResponse> {
  return request.get(`/crawl/tasks/${taskId}/items`, { params })
}

