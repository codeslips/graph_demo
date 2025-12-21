/**
 * API functions for Analysis Reports.
 */

import request from './request'
import type {
  SourceKeywordsResponse,
  ExportDataRequest,
  ExportDataResponse,
  ReportCreateRequest,
  Report,
  ReportListResponse,
} from '@/types/report'

const BASE_URL = '/media/reports'

/**
 * Get unique source keywords for a platform.
 */
export async function getSourceKeywords(platform: string): Promise<SourceKeywordsResponse> {
  // Note: request interceptor already extracts response.data
  const data = await request.get<SourceKeywordsResponse>(`${BASE_URL}/source-keywords/`, {
    params: { platform },
  })
  return data as unknown as SourceKeywordsResponse
}

/**
 * Export media data as CSV-like text for AI analysis.
 */
export async function exportMediaData(
  data: ExportDataRequest
): Promise<ExportDataResponse> {
  const result = await request.post<ExportDataResponse>(`${BASE_URL}/export-data/`, data)
  return result as unknown as ExportDataResponse
}

/**
 * Create a new analysis report.
 */
export async function createReport(data: ReportCreateRequest): Promise<Report> {
  const result = await request.post<Report>(`${BASE_URL}/`, data)
  return result as unknown as Report
}

/**
 * Get paginated list of reports.
 */
export async function getReports(
  limit: number = 20,
  offset: number = 0,
  platform?: string
): Promise<ReportListResponse> {
  const params: Record<string, unknown> = { limit, offset }
  if (platform) {
    params.platform = platform
  }
  const data = await request.get<ReportListResponse>(`${BASE_URL}/`, { params })
  return data as unknown as ReportListResponse
}

/**
 * Get a single report by ID.
 */
export async function getReport(id: string): Promise<Report> {
  const data = await request.get<Report>(`${BASE_URL}/${id}/`)
  return data as unknown as Report
}

/**
 * Delete a report by ID.
 */
export async function deleteReport(id: string): Promise<void> {
  await request.delete(`${BASE_URL}/${id}/`)
}
