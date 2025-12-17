/**
 * Graph visualization types for API interactions.
 */

export type NodeType = 'Article' | 'Channel' | 'Tag'

export interface GraphNode {
  id: string
  type: NodeType
  label: string
  properties: Record<string, unknown>
}

export interface GraphEdge {
  source: string
  target: string
  type: string
}

export interface GraphStats {
  totalNodes: number
  totalEdges: number
  nodesByType: Record<string, number>
}

export interface GraphData {
  nodes: GraphNode[]
  edges: GraphEdge[]
  stats: GraphStats
}

export interface Keyword {
  tagId: number
  name: string
  count: number
}

export interface KeywordListResponse {
  items: Keyword[]
  total: number
}

export interface SearchResult {
  id: string
  type: NodeType
  label: string
  properties: Record<string, unknown>
}

export interface SearchResponse {
  items: SearchResult[]
  total: number
}

