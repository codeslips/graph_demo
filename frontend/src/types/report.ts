/**
 * Types for Analysis Report feature.
 */

export interface SourceKeywordsResponse {
  keywords: string[]
}

export interface ExportDataRequest {
  platform: string
  source_keyword: string
  time_from?: number | null
  time_to?: number | null
}

export interface ExportDataResponse {
  csv_data: string
  record_count: number
  truncated: boolean
  total_count: number
}

export interface ReportCreateRequest {
  title: string
  platform: string
  source_keyword: string
  time_from?: number | null
  time_to?: number | null
  content: string
  record_count: number
}

export interface Report {
  id: string
  title: string
  platform: string
  source_keyword: string
  time_from?: number | null
  time_to?: number | null
  content: string
  record_count: number
  created_at: string
}

export interface ReportListItem {
  id: string
  title: string
  platform: string
  source_keyword: string
  time_from?: number | null
  time_to?: number | null
  record_count: number
  created_at: string
}

export interface ReportListResponse {
  items: ReportListItem[]
  total: number
  limit: number
  offset: number
}

export interface ReportError {
  detail: string
  code: string
}

