<script setup lang="ts">
import type { TaskStatus } from '@/types/crawl'

defineProps<{
  status: TaskStatus
  totalItems: number
}>()
</script>

<template>
  <div class="task-progress">
    <div class="progress-header">
      <span class="progress-label">
        {{ status === 'RUNNING' ? 'Crawling in progress...' : 'Crawl status' }}
      </span>
      <span class="progress-count">{{ totalItems }} items</span>
    </div>

    <div class="progress-bar-container">
      <div
        class="progress-bar"
        :class="{
          running: status === 'RUNNING',
          done: status === 'DONE',
          failed: status === 'FAILED'
        }"
      ></div>
    </div>
  </div>
</template>

<style scoped>
.task-progress {
  padding: 1rem;
  background: #1e1e2e;
  border-radius: 8px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.progress-label {
  font-size: 0.85rem;
  color: #a0a0b0;
}

.progress-count {
  font-size: 0.85rem;
  font-weight: 600;
  color: #e0e0e0;
}

.progress-bar-container {
  height: 6px;
  background: #2d2d44;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-bar.running {
  width: 60%;
  background: linear-gradient(90deg, #6366f1, #8b5cf6, #6366f1);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.progress-bar.done {
  width: 100%;
  background: #10b981;
}

.progress-bar.failed {
  width: 100%;
  background: #ef4444;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>

