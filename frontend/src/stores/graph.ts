/**
 * Pinia store for graph visualization state management.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { GraphData, GraphNode, Keyword, SearchResult } from '@/types/graph'
import { getTaskGraph, getKeywords, searchNodes } from '@/api/graph'

export const useGraphStore = defineStore('graph', () => {
  // State
  const graphData = ref<GraphData | null>(null)
  const keywords = ref<Keyword[]>([])
  const searchResults = ref<SearchResult[]>([])
  const selectedNode = ref<GraphNode | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const nodes = computed(() => graphData.value?.nodes || [])
  const edges = computed(() => graphData.value?.edges || [])
  const stats = computed(() => graphData.value?.stats || null)

  const articleNodes = computed(() =>
    nodes.value.filter((n) => n.type === 'Article')
  )

  const channelNodes = computed(() =>
    nodes.value.filter((n) => n.type === 'Channel')
  )

  const tagNodes = computed(() => nodes.value.filter((n) => n.type === 'Tag'))

  // Actions
  async function fetchGraphData(taskId: string) {
    loading.value = true
    error.value = null

    try {
      graphData.value = await getTaskGraph(taskId)
      return graphData.value
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch graph data'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchKeywords(taskId?: string, limit: number = 50) {
    loading.value = true
    error.value = null

    try {
      const response = await getKeywords({ task_id: taskId, limit })
      keywords.value = response.items
      return response
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch keywords'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function search(query: string) {
    if (!query || query.length < 2) {
      searchResults.value = []
      return
    }

    loading.value = true
    error.value = null

    try {
      const response = await searchNodes(query)
      searchResults.value = response.items
      return response
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Search failed'
      throw e
    } finally {
      loading.value = false
    }
  }

  function selectNode(node: GraphNode | null) {
    selectedNode.value = node
  }

  function clearGraph() {
    graphData.value = null
    selectedNode.value = null
    searchResults.value = []
  }

  return {
    // State
    graphData,
    keywords,
    searchResults,
    selectedNode,
    loading,
    error,

    // Getters
    nodes,
    edges,
    stats,
    articleNodes,
    channelNodes,
    tagNodes,

    // Actions
    fetchGraphData,
    fetchKeywords,
    search,
    selectNode,
    clearGraph
  }
})

