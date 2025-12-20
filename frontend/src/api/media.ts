/**
 * Media Crawl API functions
 * Provides CRUD operations for all platform entities
 */

import request from './request'
import type {
  PaginatedResponse,
  BatchDeleteRequest,
  BatchDeleteResponse,
  FilterParams,
  MediaApiStatus,
  MediaRecord,
  Platform,
} from '@/types/media'

const MEDIA_BASE_URL = '/media'

// ============== Generic CRUD Functions ==============

/**
 * List records with pagination and filtering
 */
export async function listRecords<T>(
  platform: Platform,
  entityPath: string,
  params: FilterParams = {}
): Promise<PaginatedResponse<T>> {
  const { limit = 20, offset = 0, ...filters } = params
  const queryParams = new URLSearchParams()
  queryParams.append('limit', String(limit))
  queryParams.append('offset', String(offset))
  
  if (filters.user_id) queryParams.append('user_id', filters.user_id)
  if (filters.create_time_from) queryParams.append('create_time_from', String(filters.create_time_from))
  if (filters.create_time_to) queryParams.append('create_time_to', String(filters.create_time_to))
  if (filters.source_keyword) queryParams.append('source_keyword', filters.source_keyword)
  
  return request.get(`${MEDIA_BASE_URL}/${platform}/${entityPath}/?${queryParams.toString()}`)
}

/**
 * Get a single record by ID
 */
export async function getRecord<T>(
  platform: Platform,
  entityPath: string,
  id: number
): Promise<T> {
  return request.get(`${MEDIA_BASE_URL}/${platform}/${entityPath}/${id}/`)
}

/**
 * Create a new record
 */
export async function createRecord<T>(
  platform: Platform,
  entityPath: string,
  data: Partial<T>
): Promise<T> {
  return request.post(`${MEDIA_BASE_URL}/${platform}/${entityPath}/`, data)
}

/**
 * Update an existing record
 */
export async function updateRecord<T>(
  platform: Platform,
  entityPath: string,
  id: number,
  data: Partial<T>
): Promise<T> {
  return request.put(`${MEDIA_BASE_URL}/${platform}/${entityPath}/${id}/`, data)
}

/**
 * Delete a single record
 */
export async function deleteRecord(
  platform: Platform,
  entityPath: string,
  id: number
): Promise<void> {
  return request.delete(`${MEDIA_BASE_URL}/${platform}/${entityPath}/${id}/`)
}

/**
 * Batch create records
 */
export async function batchCreateRecords<T>(
  platform: Platform,
  entityPath: string,
  data: Partial<T>[]
): Promise<T[]> {
  return request.post(`${MEDIA_BASE_URL}/${platform}/${entityPath}/batch/`, data)
}

/**
 * Batch delete records
 */
export async function batchDeleteRecords(
  platform: Platform,
  entityPath: string,
  ids: number[]
): Promise<BatchDeleteResponse> {
  return request.delete(`${MEDIA_BASE_URL}/${platform}/${entityPath}/batch/`, {
    data: { ids } as BatchDeleteRequest
  })
}

// ============== Status API ==============

/**
 * Get media crawl API status
 */
export async function getMediaApiStatus(): Promise<MediaApiStatus> {
  return request.get(`${MEDIA_BASE_URL}/status`)
}

// ============== Platform-specific convenience functions ==============

// Bilibili
export const bilibili = {
  videos: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('bilibili', 'videos', params),
    get: (id: number) => getRecord<MediaRecord>('bilibili', 'videos', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('bilibili', 'videos', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('bilibili', 'videos', id, data),
    delete: (id: number) => deleteRecord('bilibili', 'videos', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('bilibili', 'videos', ids),
  },
  comments: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('bilibili', 'comments', params),
    get: (id: number) => getRecord<MediaRecord>('bilibili', 'comments', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('bilibili', 'comments', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('bilibili', 'comments', id, data),
    delete: (id: number) => deleteRecord('bilibili', 'comments', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('bilibili', 'comments', ids),
  },
  ups: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('bilibili', 'ups', params),
    get: (id: number) => getRecord<MediaRecord>('bilibili', 'ups', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('bilibili', 'ups', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('bilibili', 'ups', id, data),
    delete: (id: number) => deleteRecord('bilibili', 'ups', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('bilibili', 'ups', ids),
  },
  contacts: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('bilibili', 'contacts', params),
    get: (id: number) => getRecord<MediaRecord>('bilibili', 'contacts', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('bilibili', 'contacts', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('bilibili', 'contacts', id, data),
    delete: (id: number) => deleteRecord('bilibili', 'contacts', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('bilibili', 'contacts', ids),
  },
  dynamics: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('bilibili', 'dynamics', params),
    get: (id: number) => getRecord<MediaRecord>('bilibili', 'dynamics', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('bilibili', 'dynamics', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('bilibili', 'dynamics', id, data),
    delete: (id: number) => deleteRecord('bilibili', 'dynamics', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('bilibili', 'dynamics', ids),
  },
}

// Douyin
export const douyin = {
  awemes: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('douyin', 'awemes', params),
    get: (id: number) => getRecord<MediaRecord>('douyin', 'awemes', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('douyin', 'awemes', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('douyin', 'awemes', id, data),
    delete: (id: number) => deleteRecord('douyin', 'awemes', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('douyin', 'awemes', ids),
  },
  comments: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('douyin', 'comments', params),
    get: (id: number) => getRecord<MediaRecord>('douyin', 'comments', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('douyin', 'comments', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('douyin', 'comments', id, data),
    delete: (id: number) => deleteRecord('douyin', 'comments', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('douyin', 'comments', ids),
  },
  creators: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('douyin', 'creators', params),
    get: (id: number) => getRecord<MediaRecord>('douyin', 'creators', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('douyin', 'creators', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('douyin', 'creators', id, data),
    delete: (id: number) => deleteRecord('douyin', 'creators', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('douyin', 'creators', ids),
  },
}

// Kuaishou
export const kuaishou = {
  videos: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('kuaishou', 'videos', params),
    get: (id: number) => getRecord<MediaRecord>('kuaishou', 'videos', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('kuaishou', 'videos', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('kuaishou', 'videos', id, data),
    delete: (id: number) => deleteRecord('kuaishou', 'videos', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('kuaishou', 'videos', ids),
  },
  comments: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('kuaishou', 'comments', params),
    get: (id: number) => getRecord<MediaRecord>('kuaishou', 'comments', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('kuaishou', 'comments', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('kuaishou', 'comments', id, data),
    delete: (id: number) => deleteRecord('kuaishou', 'comments', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('kuaishou', 'comments', ids),
  },
}

// Weibo
export const weibo = {
  notes: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('weibo', 'notes', params),
    get: (id: number) => getRecord<MediaRecord>('weibo', 'notes', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('weibo', 'notes', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('weibo', 'notes', id, data),
    delete: (id: number) => deleteRecord('weibo', 'notes', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('weibo', 'notes', ids),
  },
  comments: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('weibo', 'comments', params),
    get: (id: number) => getRecord<MediaRecord>('weibo', 'comments', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('weibo', 'comments', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('weibo', 'comments', id, data),
    delete: (id: number) => deleteRecord('weibo', 'comments', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('weibo', 'comments', ids),
  },
  creators: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('weibo', 'creators', params),
    get: (id: number) => getRecord<MediaRecord>('weibo', 'creators', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('weibo', 'creators', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('weibo', 'creators', id, data),
    delete: (id: number) => deleteRecord('weibo', 'creators', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('weibo', 'creators', ids),
  },
}

// XHS (Xiaohongshu)
export const xhs = {
  creators: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('xhs', 'creators', params),
    get: (id: number) => getRecord<MediaRecord>('xhs', 'creators', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('xhs', 'creators', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('xhs', 'creators', id, data),
    delete: (id: number) => deleteRecord('xhs', 'creators', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('xhs', 'creators', ids),
  },
  notes: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('xhs', 'notes', params),
    get: (id: number) => getRecord<MediaRecord>('xhs', 'notes', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('xhs', 'notes', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('xhs', 'notes', id, data),
    delete: (id: number) => deleteRecord('xhs', 'notes', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('xhs', 'notes', ids),
  },
  comments: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('xhs', 'comments', params),
    get: (id: number) => getRecord<MediaRecord>('xhs', 'comments', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('xhs', 'comments', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('xhs', 'comments', id, data),
    delete: (id: number) => deleteRecord('xhs', 'comments', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('xhs', 'comments', ids),
  },
}

// Tieba
export const tieba = {
  notes: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('tieba', 'notes', params),
    get: (id: number) => getRecord<MediaRecord>('tieba', 'notes', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('tieba', 'notes', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('tieba', 'notes', id, data),
    delete: (id: number) => deleteRecord('tieba', 'notes', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('tieba', 'notes', ids),
  },
  comments: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('tieba', 'comments', params),
    get: (id: number) => getRecord<MediaRecord>('tieba', 'comments', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('tieba', 'comments', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('tieba', 'comments', id, data),
    delete: (id: number) => deleteRecord('tieba', 'comments', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('tieba', 'comments', ids),
  },
  creators: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('tieba', 'creators', params),
    get: (id: number) => getRecord<MediaRecord>('tieba', 'creators', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('tieba', 'creators', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('tieba', 'creators', id, data),
    delete: (id: number) => deleteRecord('tieba', 'creators', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('tieba', 'creators', ids),
  },
}

// Zhihu
export const zhihu = {
  contents: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('zhihu', 'contents', params),
    get: (id: number) => getRecord<MediaRecord>('zhihu', 'contents', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('zhihu', 'contents', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('zhihu', 'contents', id, data),
    delete: (id: number) => deleteRecord('zhihu', 'contents', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('zhihu', 'contents', ids),
  },
  comments: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('zhihu', 'comments', params),
    get: (id: number) => getRecord<MediaRecord>('zhihu', 'comments', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('zhihu', 'comments', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('zhihu', 'comments', id, data),
    delete: (id: number) => deleteRecord('zhihu', 'comments', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('zhihu', 'comments', ids),
  },
  creators: {
    list: (params?: FilterParams) => listRecords<MediaRecord>('zhihu', 'creators', params),
    get: (id: number) => getRecord<MediaRecord>('zhihu', 'creators', id),
    create: (data: Partial<MediaRecord>) => createRecord<MediaRecord>('zhihu', 'creators', data),
    update: (id: number, data: Partial<MediaRecord>) => updateRecord<MediaRecord>('zhihu', 'creators', id, data),
    delete: (id: number) => deleteRecord('zhihu', 'creators', id),
    batchDelete: (ids: number[]) => batchDeleteRecords('zhihu', 'creators', ids),
  },
}

