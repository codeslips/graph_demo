<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { useTaskStore } from '@/stores/task'
import TaskForm from '@/components/task/TaskForm.vue'
import TaskCard from '@/components/task/TaskCard.vue'
import type { CrawlType } from '@/types/crawl'

const taskStore = useTaskStore()
const pollingInterval = ref<number | null>(null)

onMounted(async () => {
  await taskStore.fetchTasks()
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})

function startPolling() {
  pollingInterval.value = window.setInterval(async () => {
    // Only poll if there are running tasks
    if (taskStore.runningTasks.length > 0) {
      await taskStore.fetchTasks(taskStore.pagination.page)
    }
  }, 3000)
}

function stopPolling() {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
  }
}

async function handleCreateTask(data: { target_url: string; crawl_type: CrawlType }) {
  try {
    await taskStore.createNewTask(data)
  } catch (e) {
    console.error('Failed to create task:', e)
  }
}

async function handleDeleteTask(taskId: string) {
  try {
    await taskStore.removeTask(taskId)
  } catch (e) {
    console.error('Failed to delete task:', e)
  }
}
</script>

<template>
  <div class="task-list-view">
    <header class="view-header">
      <h1>爬取任务</h1>
      <p class="subtitle">管理澎湃新闻爬取任务</p>
    </header>

    <div class="content-grid">
      <aside class="sidebar">
        <TaskForm @submit="handleCreateTask" />

        <div class="stats-card">
          <h4>任务概览</h4>
          <div class="stat-row">
            <span class="stat-label">总计</span>
            <span class="stat-value">{{ taskStore.tasks.length }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">运行中</span>
            <span class="stat-value running">{{ taskStore.runningTasks.length }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">已完成</span>
            <span class="stat-value completed">{{ taskStore.completedTasks.length }}</span>
          </div>
        </div>
      </aside>

      <main class="task-list">
        <div v-if="taskStore.loading && taskStore.tasks.length === 0" class="loading-state">
          <div class="spinner"></div>
          <p>加载任务中...</p>
        </div>

        <div v-else-if="taskStore.tasks.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <h3>暂无任务</h3>
          <p>创建新任务以开始</p>
        </div>

        <div v-else class="task-grid">
          <TaskCard
            v-for="task in taskStore.tasks"
            :key="task.id"
            :task="task"
            @delete="handleDeleteTask"
          />
        </div>

        <div v-if="taskStore.pagination.hasNext" class="load-more">
          <button
            class="load-more-btn"
            :disabled="taskStore.loading"
            @click="taskStore.fetchTasks(taskStore.pagination.page + 1)"
          >
            加载更多
          </button>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.task-list-view {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(180deg, #0a0a12 0%, #12121a 100%);
}

.view-header {
  margin-bottom: 2rem;
}

.view-header h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #e0e0e0;
  background: linear-gradient(135deg, #e0e0e0 0%, #a0a0b0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  margin: 0.25rem 0 0;
  color: #6a6a80;
  font-size: 0.9rem;
}

.content-grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 2rem;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.stats-card {
  background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
  border: 1px solid #3d3d5c;
  border-radius: 12px;
  padding: 1.25rem;
}

.stats-card h4 {
  margin: 0 0 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: #a0a0b0;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #2d2d44;
}

.stat-row:last-child {
  border-bottom: none;
}

.stat-row .stat-label {
  color: #6a6a80;
  font-size: 0.85rem;
}

.stat-row .stat-value {
  font-weight: 600;
  color: #e0e0e0;
}

.stat-row .stat-value.running {
  color: #6366f1;
}

.stat-row .stat-value.completed {
  color: #10b981;
}

.task-list {
  min-height: 400px;
}

.task-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-state .spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #3d3d5c;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

.loading-state p,
.empty-state p {
  color: #6a6a80;
  margin: 0.5rem 0 0;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin: 0;
  color: #a0a0b0;
}

.load-more {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}

.load-more-btn {
  padding: 0.75rem 2rem;
  background: #2d2d44;
  border: 1px solid #3d3d5c;
  border-radius: 8px;
  color: #a0a0b0;
  cursor: pointer;
  transition: background 0.2s;
}

.load-more-btn:hover:not(:disabled) {
  background: #3d3d5c;
}

.load-more-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
