/**
 * Media graph visualization types.
 */

export type MediaPlatform = 'bilibili' | 'douyin' | 'kuaishou' | 'weibo' | 'xhs' | 'tieba' | 'zhihu'

export type MediaNodeType = 'Platform' | 'Content' | 'Keyword' | 'Comment'

export interface MediaGraphNode {
  id: string
  type: MediaNodeType
  label: string
  properties: Record<string, unknown>
}

export interface MediaGraphEdge {
  source: string
  target: string
  type: string
}

export interface MediaGraphStats {
  totalNodes: number
  totalEdges: number
  nodesByType: Record<string, number>
}

export interface MediaGraphData {
  nodes: MediaGraphNode[]
  edges: MediaGraphEdge[]
  stats: MediaGraphStats
}

export interface MediaKeyword {
  tagId: number
  name: string
  count: number
}

export interface MediaKeywordListResponse {
  items: MediaKeyword[]
  total: number
}

export interface MediaSearchResult {
  id: string
  type: string
  label: string
  properties: Record<string, unknown>
}

export interface MediaSearchResponse {
  items: MediaSearchResult[]
  total: number
}

// Sync related types
export interface SyncNeo4jRequest {
  platform?: MediaPlatform
  limit?: number
  sync?: boolean  // If true, run synchronously
}

export interface SyncNeo4jResponse {
  task_id: string | null
  message: string
  result?: {
    platforms?: Record<string, {
      content_synced: number
      keywords_synced: number
      comments_synced: number
    }>
    totals?: {
      content_synced: number
      keywords_synced: number
      comments_synced: number
    }
  } | null
}

export interface SyncStatusResponse {
  status: 'idle' | 'running'
  progress: number
  lastSyncTime: string | null
  lastResult: {
    platforms?: Record<string, {
      content_synced: number
      keywords_synced: number
      comments_synced: number
    }>
    totals?: {
      content_synced: number
      keywords_synced: number
      comments_synced: number
    }
    error?: string
  } | null
}

// Platform display info
export interface PlatformInfo {
  id: MediaPlatform
  name: string
  color: string
  icon: string
}

export const PLATFORMS: PlatformInfo[] = [
  { id: 'bilibili', name: 'Bilibili', color: '#00a1d6', icon: '📺' },
  { id: 'douyin', name: '抖音', color: '#161823', icon: '🎵' },
  { id: 'kuaishou', name: '快手', color: '#ff4500', icon: '📹' },
  { id: 'weibo', name: '微博', color: '#ff8140', icon: '📝' },
  { id: 'xhs', name: '小红书', color: '#fe2c55', icon: '📕' },
  { id: 'tieba', name: '贴吧', color: '#4879bd', icon: '💬' },
  { id: 'zhihu', name: '知乎', color: '#0066ff', icon: '❓' },
]

