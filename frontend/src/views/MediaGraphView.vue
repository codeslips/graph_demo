<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch, computed } from 'vue'
import * as echarts from 'echarts'
import { useMediaGraphStore } from '@/stores/mediaGraph'
import { PLATFORMS, type MediaGraphNode, type MediaPlatform } from '@/types/mediaGraph'

const mediaGraphStore = useMediaGraphStore()

const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

const searchQuery = ref('')

// Platform colors for content nodes
const platformColors: Record<string, string> = {
  bilibili: '#00a1d6',
  douyin: '#161823',
  kuaishou: '#ff4500',
  weibo: '#ff8140',
  xhs: '#fe2c55',
  tieba: '#4879bd',
  zhihu: '#0066ff',
}

// Node colors by type
const nodeTypeColors: Record<string, string> = {
  Platform: '#8b5cf6',
  Content: '#6366f1',
  Keyword: '#10b981',
  Comment: '#f59e0b',
}

// Node labels
const nodeLabels: Record<string, string> = {
  Platform: '平台',
  Content: '内容',
  Keyword: '关键词',
  Comment: '评论',
}

// Node sizes by type
const nodeSizes: Record<string, number> = {
  Platform: 45,
  Content: 25,
  Keyword: 20,
  Comment: 15,
}

const chartData = computed(() => {
  const categories = [
    { name: nodeLabels.Platform },
    { name: nodeLabels.Content },
    { name: nodeLabels.Keyword },
    { name: nodeLabels.Comment },
  ]

  const typeToIndex: Record<string, number> = {
    Platform: 0,
    Content: 1,
    Keyword: 2,
    Comment: 3,
  }

  const data = mediaGraphStore.nodes.map((node) => {
    // For content nodes, use platform-specific color
    let color = nodeTypeColors[node.type] || '#6366f1'
    if (node.type === 'Content' && node.properties.platform) {
      color = platformColors[node.properties.platform as string] || color
    }

    return {
      id: node.id,
      name: node.label || node.id,
      symbolSize: nodeSizes[node.type] || 20,
      category: typeToIndex[node.type] ?? 1,
      itemStyle: { color },
      properties: node.properties,
      nodeType: node.type,
    }
  })

  const links = mediaGraphStore.edges.map((edge) => ({
    source: edge.source,
    target: edge.target,
    lineStyle: {
      color: edge.type === 'HAS_CONTENT' ? '#8b5cf6' : '#10b981',
      opacity: 0.4,
      width: edge.type === 'HAS_CONTENT' ? 2 : 1,
    },
  }))

  return { data, links, categories }
})

function initChart() {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value, 'dark')
  updateChart()

  chart.on('click', 'series', (params: any) => {
    if (params.dataType === 'node') {
      const node = mediaGraphStore.nodes.find((n) => n.id === params.data.id)
      if (node) {
        mediaGraphStore.selectNode(node)
      }
    }
  })

  window.addEventListener('resize', handleResize)
}

function updateChart() {
  if (!chart) return

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: '#1e1e2e',
      borderColor: '#3d3d5c',
      textStyle: { color: '#e0e0e0' },
      formatter: (params: any) => {
        if (params.dataType === 'node') {
          const categoryName = chartData.value.categories[params.data.category]?.name || '未知'
          let extra = ''
          if (params.data.nodeType === 'Content' && params.data.properties.platform) {
            const platform = PLATFORMS.find(p => p.id === params.data.properties.platform)
            extra = `<br/>平台: ${platform?.name || params.data.properties.platform}`
          }
          return `<strong>${params.name}</strong><br/>类型: ${categoryName}${extra}`
        }
        return ''
      },
    },
    legend: {
      data: chartData.value.categories.map((c) => c.name),
      orient: 'horizontal',
      left: 'center',
      top: 10,
      textStyle: { color: '#a0a0b0' },
      itemStyle: { borderWidth: 0 },
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        data: chartData.value.data,
        links: chartData.value.links,
        categories: chartData.value.categories.map((c, i) => ({
          name: c.name,
          itemStyle: { color: Object.values(nodeTypeColors)[i] },
        })),
        roam: true,
        draggable: true,
        label: {
          show: true,
          position: 'right',
          fontSize: 10,
          color: '#a0a0b0',
          formatter: (params: any) => {
            const name = params.name || ''
            return name.length > 12 ? name.slice(0, 12) + '...' : name
          },
        },
        emphasis: {
          focus: 'adjacency',
          label: { show: true, fontSize: 12, fontWeight: 'bold' },
          lineStyle: { width: 3 },
        },
        force: {
          repulsion: 200,
          edgeLength: [60, 180],
          gravity: 0.08,
        },
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',
      },
    ],
  }

  chart.setOption(option, true)
}

function handleResize() {
  chart?.resize()
}

watch(
  () => [mediaGraphStore.nodes, mediaGraphStore.edges],
  () => {
    // Need to wait for next tick in case DOM was re-rendered
    if (chart && chartRef.value) {
      updateChart()
    }
  },
  { deep: true }
)

// Reinitialize chart when loading completes and we have data
watch(
  () => mediaGraphStore.loading,
  (loading, wasLoading) => {
    if (wasLoading && !loading && mediaGraphStore.hasData) {
      // Loading just finished, reinitialize chart after DOM updates
      setTimeout(() => {
        if (chartRef.value) {
          if (chart) {
            chart.dispose()
          }
          initChart()
        }
      }, 50)
    }
  }
)

onMounted(async () => {
  await Promise.all([
    mediaGraphStore.fetchGraphData(),
    mediaGraphStore.fetchKeywords(),
    mediaGraphStore.fetchSyncStatus(),
  ])
  initChart()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
  mediaGraphStore.stopPolling()
})

// Handlers
function handlePlatformClick(platform: MediaPlatform | null) {
  mediaGraphStore.selectPlatform(platform)
}

function handleKeywordClick(keyword: string) {
  mediaGraphStore.selectKeyword(keyword)
}

function handleSearch() {
  if (searchQuery.value.length >= 2) {
    mediaGraphStore.search(searchQuery.value)
  } else {
    mediaGraphStore.clearSearch()
  }
}

function clearFilters() {
  searchQuery.value = ''
  mediaGraphStore.selectPlatform(null)
  mediaGraphStore.selectKeyword(null)
  mediaGraphStore.clearSearch()
}

function closeNodeDetail() {
  mediaGraphStore.selectNode(null)
}

function handleSync() {
  mediaGraphStore.triggerSync()
}
</script>

<template>
  <div class="media-graph-view">
    <header class="view-header">
      <div class="header-content">
        <h1>媒体图谱</h1>
        <p class="subtitle">
          <template v-if="mediaGraphStore.selectedPlatform">
            <span class="highlight">{{ PLATFORMS.find(p => p.id === mediaGraphStore.selectedPlatform)?.name }}</span>
            平台数据
          </template>
          <template v-else-if="mediaGraphStore.selectedKeyword">
            关键词: <span class="highlight">{{ mediaGraphStore.selectedKeyword }}</span>
          </template>
          <template v-else>
            探索社交媒体内容关系
          </template>
        </p>
      </div>
      
      <div class="header-actions">
        <button 
          class="sync-btn"
          :disabled="mediaGraphStore.syncing"
          @click="handleSync"
        >
          <span v-if="mediaGraphStore.syncing" class="sync-icon spinning">⟳</span>
          <span v-else class="sync-icon">⟳</span>
          {{ mediaGraphStore.syncing ? `同步中 ${mediaGraphStore.syncStatus.progress}%` : '同步到 Neo4j' }}
        </button>
      </div>
    </header>

    <div class="graph-layout">
      <!-- Sidebar -->
      <aside class="sidebar">
        <!-- Search -->
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索关键词..."
            @input="handleSearch"
          />
        </div>

        <!-- Search Results -->
        <div v-if="mediaGraphStore.searchResults.length > 0" class="search-results">
          <h4>搜索结果</h4>
          <div
            v-for="result in mediaGraphStore.searchResults"
            :key="result.id"
            class="search-result-item"
            @click="handleKeywordClick(result.label)"
          >
            <span class="result-type keyword">Keyword</span>
            <span class="result-label">{{ result.label }}</span>
            <span class="result-count">{{ result.properties.count }}</span>
          </div>
        </div>

        <!-- Platform Tabs -->
        <div class="platform-section">
          <h4>平台筛选</h4>
          <div class="platform-tabs">
            <button
              class="platform-tab"
              :class="{ active: !mediaGraphStore.selectedPlatform }"
              @click="handlePlatformClick(null)"
            >
              🌐 全部
            </button>
            <button
              v-for="platform in PLATFORMS"
              :key="platform.id"
              class="platform-tab"
              :class="{ active: mediaGraphStore.selectedPlatform === platform.id }"
              :style="{ '--platform-color': platform.color }"
              @click="handlePlatformClick(platform.id)"
            >
              {{ platform.icon }} {{ platform.name }}
            </button>
          </div>
        </div>

        <!-- Clear Filters -->
        <button
          v-if="mediaGraphStore.selectedPlatform || mediaGraphStore.selectedKeyword"
          class="clear-filters-btn"
          @click="clearFilters"
        >
          ✕ 清除筛选
        </button>

        <!-- Legend & Stats -->
        <div class="legend-section">
          <h4>图例</h4>
          <div class="legend-items">
            <div class="legend-item">
              <span class="legend-dot" style="background: #8b5cf6"></span>
              <span>平台 ({{ mediaGraphStore.stats.nodesByType['Platform'] || 0 }})</span>
            </div>
            <div class="legend-item">
              <span class="legend-dot" style="background: #6366f1"></span>
              <span>内容 ({{ mediaGraphStore.stats.nodesByType['Content'] || 0 }})</span>
            </div>
            <div class="legend-item">
              <span class="legend-dot" style="background: #10b981"></span>
              <span>关键词 ({{ mediaGraphStore.stats.nodesByType['Keyword'] || 0 }})</span>
            </div>
          </div>
          <div class="stats-summary">
            <span>节点: {{ mediaGraphStore.stats.totalNodes }}</span>
            <span>边: {{ mediaGraphStore.stats.totalEdges }}</span>
          </div>
        </div>

        <!-- Keywords Cloud -->
        <div class="keywords-section">
          <h4>热门关键词</h4>
          <div v-if="mediaGraphStore.keywordsLoading" class="loading-small">加载中...</div>
          <div v-else class="keyword-cloud">
            <span
              v-for="keyword in mediaGraphStore.keywords.slice(0, 20)"
              :key="keyword.name"
              class="keyword-tag"
              :class="{ active: mediaGraphStore.selectedKeyword === keyword.name }"
              @click="handleKeywordClick(keyword.name)"
            >
              {{ keyword.name }}
              <span class="keyword-count">{{ keyword.count }}</span>
            </span>
          </div>
        </div>
      </aside>

      <!-- Graph Container -->
      <main class="graph-container">
        <div v-if="mediaGraphStore.loading" class="loading-overlay">
          <div class="spinner"></div>
          <p>加载图谱数据...</p>
        </div>

        <div v-else-if="!mediaGraphStore.hasData" class="empty-state">
          <div class="empty-icon">🕸️</div>
          <h3>暂无图谱数据</h3>
          <p>请先同步媒体数据到 Neo4j</p>
          <button class="sync-btn-large" @click="handleSync" :disabled="mediaGraphStore.syncing">
            {{ mediaGraphStore.syncing ? '同步中...' : '开始同步' }}
          </button>
        </div>

        <div v-else ref="chartRef" class="graph-canvas"></div>

        <!-- Node Detail Panel -->
        <div v-if="mediaGraphStore.selectedNode" class="node-detail-panel">
          <div class="panel-header">
            <h3>{{ mediaGraphStore.selectedNode.label }}</h3>
            <button class="close-btn" @click="closeNodeDetail">✕</button>
          </div>
          <div class="panel-content">
            <div class="detail-row">
              <span class="label">类型:</span>
              <span class="value">{{ nodeLabels[mediaGraphStore.selectedNode.type] || mediaGraphStore.selectedNode.type }}</span>
            </div>
            <template v-if="mediaGraphStore.selectedNode.type === 'Content'">
              <div class="detail-row" v-if="mediaGraphStore.selectedNode.properties.platform">
                <span class="label">平台:</span>
                <span class="value">{{ PLATFORMS.find(p => p.id === mediaGraphStore.selectedNode?.properties.platform)?.name }}</span>
              </div>
              <div class="detail-row" v-if="mediaGraphStore.selectedNode.properties.author">
                <span class="label">作者:</span>
                <span class="value">{{ mediaGraphStore.selectedNode.properties.author }}</span>
              </div>
              <div class="detail-row" v-if="mediaGraphStore.selectedNode.properties.createTime">
                <span class="label">时间:</span>
                <span class="value">{{ mediaGraphStore.selectedNode.properties.createTime }}</span>
              </div>
              <div class="detail-row" v-if="mediaGraphStore.selectedNode.properties.likedCount">
                <span class="label">点赞:</span>
                <span class="value">{{ mediaGraphStore.selectedNode.properties.likedCount }}</span>
              </div>
              <div class="detail-row" v-if="mediaGraphStore.selectedNode.properties.url">
                <a :href="mediaGraphStore.selectedNode.properties.url as string" target="_blank" class="link">
                  查看原文 →
                </a>
              </div>
            </template>
            <template v-else-if="mediaGraphStore.selectedNode.type === 'Keyword'">
              <div class="detail-row">
                <span class="label">关联内容:</span>
                <span class="value">{{ mediaGraphStore.selectedNode.properties.count || '-' }} 条</span>
              </div>
            </template>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.media-graph-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, #0a0a12 0%, #12121a 100%);
}

.view-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #2d2d44;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-content h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #e0e0e0;
  background: linear-gradient(135deg, #e0e0e0 0%, #a0a0b0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  margin: 0.25rem 0 0;
  font-size: 0.85rem;
  color: #6a6a80;
}

.subtitle .highlight {
  color: #8b5cf6;
}

.sync-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.sync-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.sync-btn:not(:disabled):hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.sync-icon {
  font-size: 1rem;
}

.sync-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.graph-layout {
  flex: 1;
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 0;
}

.sidebar {
  padding: 1.5rem;
  border-right: 1px solid #2d2d44;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  overflow-y: auto;
  max-height: calc(100vh - 100px);
}

.search-box input {
  width: 100%;
  padding: 0.625rem 0.875rem;
  background: #1e1e2e;
  border: 1px solid #3d3d5c;
  border-radius: 8px;
  color: #e0e0e0;
  font-size: 0.9rem;
}

.search-box input:focus {
  outline: none;
  border-color: #6366f1;
}

.search-box input::placeholder {
  color: #5a5a70;
}

.search-results {
  background: #1e1e2e;
  border-radius: 8px;
  padding: 0.75rem;
}

.search-results h4,
.platform-section h4,
.legend-section h4,
.keywords-section h4 {
  margin: 0 0 0.75rem;
  font-size: 0.75rem;
  color: #6a6a80;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.search-result-item:hover {
  background: #2d2d44;
}

.result-type {
  font-size: 0.6rem;
  padding: 0.1rem 0.35rem;
  border-radius: 3px;
  font-weight: 600;
  text-transform: uppercase;
}

.result-type.keyword {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.result-label {
  flex: 1;
  font-size: 0.85rem;
  color: #b0b0c0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.result-count {
  font-size: 0.75rem;
  color: #6a6a80;
}

.platform-tabs {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.platform-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: #1e1e2e;
  border: 1px solid #3d3d5c;
  border-radius: 6px;
  color: #a0a0b0;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.platform-tab:hover {
  background: #2d2d44;
  border-color: #4d4d6c;
}

.platform-tab.active {
  background: rgba(139, 92, 246, 0.15);
  border-color: #8b5cf6;
  color: #e0e0e0;
}

.clear-filters-btn {
  padding: 0.5rem 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 6px;
  color: #f87171;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-filters-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #a0a0b0;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.stats-summary {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #2d2d44;
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: #6a6a80;
}

.keyword-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.keyword-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.25rem 0.5rem;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 4px;
  font-size: 0.75rem;
  color: #a0a0b0;
  cursor: pointer;
  transition: all 0.2s;
}

.keyword-tag:hover {
  background: rgba(99, 102, 241, 0.2);
}

.keyword-tag.active {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.keyword-count {
  font-size: 0.65rem;
  color: #6366f1;
  font-weight: 600;
}

.loading-small {
  font-size: 0.8rem;
  color: #6a6a80;
}

.graph-container {
  position: relative;
  flex: 1;
  min-height: calc(100vh - 100px);
  background: radial-gradient(ellipse at center, #1a1a28 0%, #0a0a12 100%);
}

.graph-canvas {
  width: 100%;
  height: 100%;
  min-height: 500px;
}

.loading-overlay,
.empty-state {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.spinner {
  width: 2.5rem;
  height: 2.5rem;
  border: 3px solid #3d3d5c;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-overlay p,
.empty-state p {
  margin-top: 1rem;
  color: #6a6a80;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin: 0;
  color: #a0a0b0;
}

.sync-btn-large {
  margin-top: 1.5rem;
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.sync-btn-large:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.sync-btn-large:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
}

.node-detail-panel {
  position: absolute;
  right: 1rem;
  top: 1rem;
  width: 300px;
  background: #1e1e2e;
  border: 1px solid #3d3d5c;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #2d2d44;
}

.panel-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #e0e0e0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.close-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: #6a6a80;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #2d2d44;
  color: #e0e0e0;
}

.panel-content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-row {
  display: flex;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.detail-row .label {
  color: #6a6a80;
  min-width: 60px;
}

.detail-row .value {
  color: #b0b0c0;
  flex: 1;
}

.detail-row .link {
  color: #8b5cf6;
  text-decoration: none;
  transition: color 0.2s;
}

.detail-row .link:hover {
  color: #a78bfa;
}

@media (max-width: 900px) {
  .graph-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none;
  }

  .node-detail-panel {
    left: 1rem;
    right: 1rem;
    width: auto;
    bottom: 1rem;
    top: auto;
  }
}
</style>

