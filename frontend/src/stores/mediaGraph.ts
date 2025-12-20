/**
 * Media Graph Pinia store.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getMediaGraph,
  getMediaKeywords,
  searchMediaKeywords,
  triggerMediaSync,
  getMediaSyncStatus,
} from '@/api/mediaGraph'
import type {
  MediaGraphNode,
  MediaGraphEdge,
  MediaGraphStats,
  MediaKeyword,
  MediaSearchResult,
  MediaPlatform,
  SyncStatusResponse,
} from '@/types/mediaGraph'

export const useMediaGraphStore = defineStore('mediaGraph', () => {
  // Graph data state
  const nodes = ref<MediaGraphNode[]>([])
  const edges = ref<MediaGraphEdge[]>([])
  const stats = ref<MediaGraphStats>({
    totalNodes: 0,
    totalEdges: 0,
    nodesByType: {},
  })

  // Keywords state
  const keywords = ref<MediaKeyword[]>([])

  // Search state
  const searchResults = ref<MediaSearchResult[]>([])
  const searchQuery = ref('')

  // Filter state
  const selectedPlatform = ref<MediaPlatform | null>(null)
  const selectedKeyword = ref<string | null>(null)

  // Selected node for detail panel
  const selectedNode = ref<MediaGraphNode | null>(null)

  // Loading states
  const loading = ref(false)
  const keywordsLoading = ref(false)
  const searchLoading = ref(false)

  // Sync state
  const syncStatus = ref<SyncStatusResponse>({
    status: 'idle',
    progress: 0,
    lastSyncTime: null,
    lastResult: null,
  })
  const syncing = ref(false)

  // Error state
  const error = ref<string | null>(null)

  // Computed
  const hasData = computed(() => nodes.value.length > 0)
  const isSyncing = computed(() => syncStatus.value.status === 'running')

  // Actions
  async function fetchGraphData(platform?: MediaPlatform, keyword?: string) {
    loading.value = true
    error.value = null

    try {
      const data = await getMediaGraph({
        platform: platform || undefined,
        keyword: keyword || undefined,
        limit: 200,
      })

      nodes.value = data.nodes
      edges.value = data.edges
      stats.value = data.stats
    } catch (e) {
      console.error('Failed to fetch media graph data:', e)
      error.value = 'Failed to load graph data'
      nodes.value = []
      edges.value = []
      stats.value = { totalNodes: 0, totalEdges: 0, nodesByType: {} }
    } finally {
      loading.value = false
    }
  }

  async function fetchKeywords(platform?: MediaPlatform) {
    keywordsLoading.value = true

    try {
      const response = await getMediaKeywords({
        platform: platform || undefined,
        limit: 50,
      })
      keywords.value = response.items
    } catch (e) {
      console.error('Failed to fetch media keywords:', e)
      keywords.value = []
    } finally {
      keywordsLoading.value = false
    }
  }

  async function search(query: string) {
    if (!query || query.length < 2) {
      searchResults.value = []
      return
    }

    searchLoading.value = true
    searchQuery.value = query

    try {
      const response = await searchMediaKeywords(query, 20)
      searchResults.value = response.items
    } catch (e) {
      console.error('Failed to search media keywords:', e)
      searchResults.value = []
    } finally {
      searchLoading.value = false
    }
  }

  function clearSearch() {
    searchQuery.value = ''
    searchResults.value = []
  }

  function selectPlatform(platform: MediaPlatform | null) {
    selectedPlatform.value = platform
    selectedKeyword.value = null
    fetchGraphData(platform || undefined, undefined)
    fetchKeywords(platform || undefined)
  }

  function selectKeyword(keyword: string | null) {
    selectedKeyword.value = keyword
    fetchGraphData(selectedPlatform.value || undefined, keyword || undefined)
  }

  function selectNode(node: MediaGraphNode | null) {
    selectedNode.value = node
  }

  async function triggerSync(platform?: MediaPlatform, limit?: number) {
    syncing.value = true
    error.value = null

    try {
      const response = await triggerMediaSync({
        platform: platform || undefined,
        limit: limit || undefined,
      }, true)  // Use sync mode
      
      // Sync mode returns result directly
      if (response.result) {
        syncStatus.value = {
          status: 'idle',
          progress: 100,
          lastSyncTime: new Date().toISOString(),
          lastResult: response.result,
        }
        syncing.value = false
        
        // Refresh graph data after sync
        await fetchGraphData(selectedPlatform.value || undefined, selectedKeyword.value || undefined)
        await fetchKeywords(selectedPlatform.value || undefined)
      } else if (response.task_id) {
        // Async mode - poll for status
        pollSyncStatus()
      }
    } catch (e) {
      console.error('Failed to trigger sync:', e)
      error.value = 'Failed to start sync'
      syncing.value = false
    }
  }

  async function fetchSyncStatus() {
    try {
      syncStatus.value = await getMediaSyncStatus()
      syncing.value = syncStatus.value.status === 'running'
    } catch (e) {
      console.error('Failed to fetch sync status:', e)
    }
  }

  let syncPollInterval: ReturnType<typeof setInterval> | null = null

  function pollSyncStatus() {
    // Clear any existing interval
    if (syncPollInterval) {
      clearInterval(syncPollInterval)
    }

    // Poll every 2 seconds
    syncPollInterval = setInterval(async () => {
      await fetchSyncStatus()

      if (syncStatus.value.status === 'idle') {
        // Sync completed, stop polling
        if (syncPollInterval) {
          clearInterval(syncPollInterval)
          syncPollInterval = null
        }
        syncing.value = false

        // Refresh graph data
        fetchGraphData(selectedPlatform.value || undefined, selectedKeyword.value || undefined)
        fetchKeywords(selectedPlatform.value || undefined)
      }
    }, 2000)
  }

  function stopPolling() {
    if (syncPollInterval) {
      clearInterval(syncPollInterval)
      syncPollInterval = null
    }
  }

  function reset() {
    nodes.value = []
    edges.value = []
    stats.value = { totalNodes: 0, totalEdges: 0, nodesByType: {} }
    keywords.value = []
    searchResults.value = []
    selectedPlatform.value = null
    selectedKeyword.value = null
    selectedNode.value = null
    error.value = null
    stopPolling()
  }

  return {
    // State
    nodes,
    edges,
    stats,
    keywords,
    searchResults,
    searchQuery,
    selectedPlatform,
    selectedKeyword,
    selectedNode,
    loading,
    keywordsLoading,
    searchLoading,
    syncStatus,
    syncing,
    error,

    // Computed
    hasData,
    isSyncing,

    // Actions
    fetchGraphData,
    fetchKeywords,
    search,
    clearSearch,
    selectPlatform,
    selectKeyword,
    selectNode,
    triggerSync,
    fetchSyncStatus,
    pollSyncStatus,
    stopPolling,
    reset,
  }
})

