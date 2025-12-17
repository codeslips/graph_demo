<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import StatusBadge from '@/components/common/StatusBadge.vue'
import TaskProgress from '@/components/task/TaskProgress.vue'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()

const taskId = computed(() => route.params.id as string)

onMounted(async () => {
  if (taskId.value) {
    await taskStore.fetchTask(taskId.value)
    await taskStore.fetchTaskItems(taskId.value)
  }
})

function goBack() {
  router.push('/tasks')
}

function viewGraph() {
  if (taskStore.currentTask?.status === 'DONE') {
    router.push(`/graph/${taskId.value}`)
  }
}

function formatDate(dateStr: string | null) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}
</script>

<template>
  <div class="task-detail-view">
    <header class="view-header">
      <button class="back-btn" @click="goBack">← Back to Tasks</button>
      <div class="header-content" v-if="taskStore.currentTask">
        <div class="header-left">
          <h1>Task Details</h1>
          <StatusBadge :status="taskStore.currentTask.status" />
        </div>
        <button
          v-if="taskStore.currentTask.status === 'DONE' && taskStore.currentTask.total_items > 0"
          class="view-graph-btn"
          @click="viewGraph"
        >
          View Graph →
        </button>
      </div>
    </header>

    <div v-if="taskStore.loading && !taskStore.currentTask" class="loading-state">
      <div class="spinner"></div>
      <p>Loading task details...</p>
    </div>

    <template v-else-if="taskStore.currentTask">
      <section class="task-info">
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Target URL</span>
            <a :href="taskStore.currentTask.target_url" target="_blank" class="info-value link">
              {{ taskStore.currentTask.target_url }}
            </a>
          </div>

          <div class="info-item">
            <span class="info-label">Crawl Type</span>
            <span class="info-value">{{ taskStore.currentTask.crawl_type }}</span>
          </div>

          <div class="info-item">
            <span class="info-label">Created</span>
            <span class="info-value">{{ formatDate(taskStore.currentTask.created_at) }}</span>
          </div>

          <div class="info-item">
            <span class="info-label">Started</span>
            <span class="info-value">{{ formatDate(taskStore.currentTask.started_at) }}</span>
          </div>

          <div class="info-item">
            <span class="info-label">Finished</span>
            <span class="info-value">{{ formatDate(taskStore.currentTask.finished_at) }}</span>
          </div>

          <div class="info-item">
            <span class="info-label">Total Items</span>
            <span class="info-value highlight">{{ taskStore.currentTask.total_items }}</span>
          </div>
        </div>

        <TaskProgress
          v-if="taskStore.currentTask.status === 'RUNNING'"
          :status="taskStore.currentTask.status"
          :total-items="taskStore.currentTask.total_items"
        />

        <div v-if="taskStore.currentTask.error_message" class="error-box">
          <strong>Error:</strong> {{ taskStore.currentTask.error_message }}
        </div>
      </section>

      <section class="items-section">
        <h2>Crawled Items ({{ taskStore.currentItems.length }})</h2>

        <div v-if="taskStore.currentItems.length === 0" class="empty-items">
          <p>No items crawled yet</p>
        </div>

        <div v-else class="items-list">
          <div v-for="item in taskStore.currentItems" :key="item.id" class="item-card">
            <div class="item-header">
              <span class="item-channel">{{ item.channel_name }}</span>
              <span class="item-date">{{ formatDate(item.publish_time) }}</span>
            </div>
            <h3 class="item-title">
              <a :href="item.url" target="_blank">{{ item.title }}</a>
            </h3>
            <p class="item-summary">{{ item.summary }}</p>
            <div class="item-tags">
              <span v-for="tag in item.tags" :key="tag.tagId" class="tag">
                {{ tag.tag }}
              </span>
            </div>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
.task-detail-view {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(180deg, #0a0a12 0%, #12121a 100%);
}

.view-header {
  margin-bottom: 2rem;
}

.back-btn {
  background: none;
  border: none;
  color: #6a6a80;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0;
  margin-bottom: 1rem;
  transition: color 0.2s;
}

.back-btn:hover {
  color: #a0a0b0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-left h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #e0e0e0;
}

.view-graph-btn {
  padding: 0.625rem 1.25rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.view-graph-btn:hover {
  opacity: 0.9;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4rem;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #3d3d5c;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-state p {
  margin-top: 1rem;
  color: #6a6a80;
}

.task-info {
  background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
  border: 1px solid #3d3d5c;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.75rem;
  color: #6a6a80;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 0.95rem;
  color: #e0e0e0;
}

.info-value.link {
  color: #6366f1;
  text-decoration: none;
  word-break: break-all;
}

.info-value.link:hover {
  text-decoration: underline;
}

.info-value.highlight {
  font-size: 1.25rem;
  font-weight: 700;
  color: #8b5cf6;
}

.error-box {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #f87171;
  font-size: 0.9rem;
}

.items-section h2 {
  font-size: 1.1rem;
  color: #e0e0e0;
  margin: 0 0 1rem;
}

.empty-items {
  padding: 2rem;
  text-align: center;
  color: #6a6a80;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.item-card {
  background: #1e1e2e;
  border: 1px solid #3d3d5c;
  border-radius: 10px;
  padding: 1rem;
}

.item-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.item-channel {
  font-size: 0.75rem;
  color: #8b5cf6;
  font-weight: 500;
}

.item-date {
  font-size: 0.75rem;
  color: #6a6a80;
}

.item-title {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  line-height: 1.4;
}

.item-title a {
  color: #e0e0e0;
  text-decoration: none;
}

.item-title a:hover {
  color: #6366f1;
}

.item-summary {
  margin: 0 0 0.75rem;
  font-size: 0.85rem;
  color: #8a8a9a;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  padding: 0.2rem 0.5rem;
  background: rgba(99, 102, 241, 0.15);
  border-radius: 4px;
  font-size: 0.7rem;
  color: #8b5cf6;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
