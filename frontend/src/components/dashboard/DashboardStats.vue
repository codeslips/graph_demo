<script setup lang="ts">
import type { DashboardStats } from '@/types/dashboard'

defineProps<{
  stats: DashboardStats
  loading: boolean
}>()

const statItems = [
  { key: 'totalRecords', icon: '📊', label: '媒体数据', color: '#6366f1' },
  { key: 'totalReports', icon: '📋', label: '分析报告', color: '#10b981' },
  { key: 'activePlatforms', icon: '📱', label: '活跃平台', color: '#f59e0b' },
  { key: 'crawlerStatus', icon: '🕷️', label: '爬虫状态', color: '#8b5cf6' },
]

function formatValue(key: string, stats: DashboardStats): string {
  if (key === 'crawlerStatus') {
    return stats.crawlerStatus === 'running' ? '运行中' : '空闲'
  }
  const value = stats[key as keyof DashboardStats]
  if (typeof value === 'number') {
    return value.toLocaleString()
  }
  return String(value)
}
</script>

<template>
  <div class="stats-grid">
    <div
      v-for="item in statItems"
      :key="item.key"
      class="stat-card"
      :style="{ '--accent-color': item.color }"
    >
      <div class="stat-icon">{{ item.icon }}</div>
      <div class="stat-content">
        <div v-if="loading" class="stat-value loading">
          <div class="skeleton"></div>
        </div>
        <div v-else class="stat-value">
          {{ formatValue(item.key, stats) }}
        </div>
        <div class="stat-label">{{ item.label }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(12px);
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: var(--accent-color);
  transform: translateY(-4px);
  box-shadow: 0 12px 24px -12px var(--accent-color);
}

.stat-icon {
  font-size: 2.25rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: #f8fafc;
  line-height: 1;
  letter-spacing: -0.025em;
}

.stat-value.loading {
  height: 1.75rem;
}

.skeleton {
  width: 60px;
  height: 100%;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.03) 0%,
    rgba(255, 255, 255, 0.08) 50%,
    rgba(255, 255, 255, 0.03) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.stat-label {
  font-size: 0.8125rem;
  color: #94a3b8;
  margin-top: 0.375rem;
  font-weight: 500;
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 1rem 1.25rem;
  }
}
</style>

