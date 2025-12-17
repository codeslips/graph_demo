<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useGraphStore } from '@/stores/graph'
import { useTaskStore } from '@/stores/task'
import GraphCanvas from '@/components/graph/GraphCanvas.vue'
import NodeDetail from '@/components/graph/NodeDetail.vue'
import GraphLegend from '@/components/graph/GraphLegend.vue'
import type { GraphNode } from '@/types/graph'

const route = useRoute()
const router = useRouter()
const graphStore = useGraphStore()
const taskStore = useTaskStore()

const taskId = computed(() => route.params.id as string)
const searchQuery = ref('')

onMounted(async () => {
  if (taskId.value) {
    await Promise.all([
      taskStore.fetchTask(taskId.value),
      graphStore.fetchGraphData(taskId.value),
      graphStore.fetchKeywords(taskId.value)
    ])
  }
})

function goBack() {
  router.push('/tasks')
}

function handleNodeClick(node: GraphNode) {
  graphStore.selectNode(node)
}

function closeNodeDetail() {
  graphStore.selectNode(null)
}

async function handleSearch() {
  if (searchQuery.value.length >= 2) {
    await graphStore.search(searchQuery.value)
  }
}
</script>

<template>
  <div class="graph-view">
    <header class="view-header">
      <button class="back-btn" @click="goBack">← 返回任务列表</button>
      <div class="header-content">
        <div>
          <h1>知识图谱</h1>
          <p v-if="taskStore.currentTask" class="task-info">
            {{ taskStore.currentTask.total_items }} 篇文章来自
            <span class="highlight">{{ taskStore.currentTask.target_url }}</span>
          </p>
        </div>
      </div>
    </header>

    <div class="graph-layout">
      <aside class="sidebar">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索节点..."
            @input="handleSearch"
          />
        </div>

        <div v-if="graphStore.searchResults.length > 0" class="search-results">
          <h4>搜索结果</h4>
          <div
            v-for="result in graphStore.searchResults"
            :key="result.id"
            class="search-result-item"
            @click="graphStore.selectNode(result as GraphNode)"
          >
            <span class="result-type" :class="result.type.toLowerCase()">
              {{ result.type }}
            </span>
            <span class="result-label">{{ result.label }}</span>
          </div>
        </div>

        <GraphLegend :stats="graphStore.stats" />

        <div class="keywords-section">
          <h4>热门标签</h4>
          <div class="keyword-cloud">
            <span
              v-for="keyword in graphStore.keywords.slice(0, 15)"
              :key="keyword.tagId"
              class="keyword-tag"
            >
              {{ keyword.name }}
              <span class="keyword-count">{{ keyword.count }}</span>
            </span>
          </div>
        </div>
      </aside>

      <main class="graph-container">
        <div v-if="graphStore.loading" class="loading-overlay">
          <div class="spinner"></div>
          <p>加载图谱数据...</p>
        </div>

        <div v-else-if="graphStore.nodes.length === 0" class="empty-state">
          <div class="empty-icon">🕸️</div>
          <h3>暂无图谱数据</h3>
          <p>该任务暂无同步数据</p>
        </div>

        <template v-else>
          <GraphCanvas
            :nodes="graphStore.nodes"
            :edges="graphStore.edges"
            @node-click="handleNodeClick"
          />
          <NodeDetail :node="graphStore.selectedNode" @close="closeNodeDetail" />
        </template>
      </main>
    </div>
  </div>
</template>

<style scoped>
.graph-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, #0a0a12 0%, #12121a 100%);
}

.view-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #2d2d44;
}

.back-btn {
  background: none;
  border: none;
  color: #6a6a80;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0;
  margin-bottom: 0.75rem;
  transition: color 0.2s;
}

.back-btn:hover {
  color: #a0a0b0;
}

.header-content h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #e0e0e0;
}

.task-info {
  margin: 0.25rem 0 0;
  font-size: 0.85rem;
  color: #6a6a80;
}

.task-info .highlight {
  color: #8b5cf6;
}

.graph-layout {
  flex: 1;
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 0;
}

.sidebar {
  padding: 1.5rem;
  border-right: 1px solid #2d2d44;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  overflow-y: auto;
  max-height: calc(100vh - 120px);
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

.search-results h4 {
  margin: 0 0 0.5rem;
  font-size: 0.75rem;
  color: #6a6a80;
  text-transform: uppercase;
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
  font-size: 0.65rem;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  font-weight: 600;
  text-transform: uppercase;
}

.result-type.channel {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.result-type.article {
  background: rgba(99, 102, 241, 0.2);
  color: #8b5cf6;
}

.result-type.tag {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.result-label {
  font-size: 0.85rem;
  color: #b0b0c0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.keywords-section h4 {
  margin: 0 0 0.75rem;
  font-size: 0.75rem;
  color: #6a6a80;
  text-transform: uppercase;
  letter-spacing: 0.05em;
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
}

.keyword-count {
  font-size: 0.65rem;
  color: #6366f1;
  font-weight: 600;
}

.graph-container {
  position: relative;
  flex: 1;
  min-height: calc(100vh - 120px);
  background: radial-gradient(ellipse at center, #1a1a28 0%, #0a0a12 100%);
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

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 900px) {
  .graph-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none;
  }
}
</style>
