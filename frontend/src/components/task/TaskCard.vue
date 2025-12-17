<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import type { CrawlTask } from '@/types/crawl'
import StatusBadge from '@/components/common/StatusBadge.vue'

const props = defineProps<{
  task: CrawlTask
}>()

const emit = defineEmits<{
  delete: [taskId: string]
}>()

const router = useRouter()

const formattedDate = computed(() => {
  const date = new Date(props.task.created_at)
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
})

const canViewGraph = computed(() => {
  return props.task.status === 'DONE' && props.task.total_items > 0
})

function viewGraph() {
  if (canViewGraph.value) {
    router.push(`/graph/${props.task.id}`)
  }
}

function handleDelete() {
  if (confirm('确定要删除此任务吗？')) {
    emit('delete', props.task.id)
  }
}
</script>

<template>
  <div class="task-card" :class="{ clickable: canViewGraph }" @click="viewGraph">
    <div class="card-header">
      <StatusBadge :status="task.status" />
      <span class="task-date">{{ formattedDate }}</span>
    </div>

    <div class="card-body">
      <p class="task-url" :title="task.target_url">
        {{ task.target_url }}
      </p>

      <div class="task-stats">
        <span class="stat">
          <span class="stat-value">{{ task.total_items }}</span>
          <span class="stat-label">条目</span>
        </span>
        <span class="stat">
          <span class="stat-value">{{ task.crawl_type }}</span>
          <span class="stat-label">类型</span>
        </span>
      </div>

      <p v-if="task.error_message" class="error-message">
        {{ task.error_message }}
      </p>
    </div>

    <div class="card-actions">
      <button v-if="canViewGraph" class="action-btn primary" @click.stop="viewGraph">
        查看图谱
      </button>
      <button class="action-btn danger" @click.stop="handleDelete">删除</button>
    </div>
  </div>
</template>

<style scoped>
.task-card {
  background: linear-gradient(135deg, #1e1e2e 0%, #252538 100%);
  border: 1px solid #3d3d5c;
  border-radius: 12px;
  padding: 1rem;
  transition: border-color 0.2s, transform 0.2s;
}

.task-card.clickable {
  cursor: pointer;
}

.task-card.clickable:hover {
  border-color: #6366f1;
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.task-date {
  font-size: 0.75rem;
  color: #6a6a80;
}

.card-body {
  margin-bottom: 0.75rem;
}

.task-url {
  margin: 0 0 0.75rem;
  font-size: 0.85rem;
  color: #b0b0c0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.task-stats {
  display: flex;
  gap: 1.5rem;
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e0e0e0;
}

.stat-label {
  font-size: 0.7rem;
  color: #6a6a80;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.error-message {
  margin: 0.75rem 0 0;
  padding: 0.5rem;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 6px;
  font-size: 0.8rem;
  color: #f87171;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
}

.action-btn:hover {
  opacity: 0.85;
}

.action-btn.primary {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
}

.action-btn.danger {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}
</style>

