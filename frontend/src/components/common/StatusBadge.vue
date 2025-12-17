<script setup lang="ts">
import type { TaskStatus } from '@/types/crawl'

const props = defineProps<{
  status: TaskStatus
}>()

const statusConfig = {
  PENDING: { label: '等待中', class: 'status-pending' },
  RUNNING: { label: '运行中', class: 'status-running' },
  DONE: { label: '已完成', class: 'status-done' },
  FAILED: { label: '失败', class: 'status-failed' }
}

const config = statusConfig[props.status] || statusConfig.PENDING
</script>

<template>
  <span class="status-badge" :class="config.class">
    <span v-if="status === 'RUNNING'" class="spinner"></span>
    {{ config.label }}
  </span>
</template>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.status-pending {
  background: #fef3c7;
  color: #92400e;
}

.status-running {
  background: #dbeafe;
  color: #1e40af;
}

.status-done {
  background: #d1fae5;
  color: #065f46;
}

.status-failed {
  background: #fee2e2;
  color: #991b1b;
}

.spinner {
  width: 0.75rem;
  height: 0.75rem;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>

