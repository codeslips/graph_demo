<script setup lang="ts">
import type { GraphStats } from '@/types/graph'

defineProps<{
  stats: GraphStats | null
}>()

const legendItems = [
  { type: 'Channel', label: '频道', color: '#f59e0b' },
  { type: 'Article', label: '文章', color: '#6366f1' },
  { type: 'Tag', label: '标签', color: '#10b981' }
]
</script>

<template>
  <div class="graph-legend">
    <div class="legend-title">Graph Legend</div>

    <div class="legend-items">
      <div v-for="item in legendItems" :key="item.type" class="legend-item">
        <span class="legend-dot" :style="{ backgroundColor: item.color }"></span>
        <span class="legend-label">{{ item.label }}</span>
        <span v-if="stats" class="legend-count">
          {{ stats.nodesByType[item.type] || 0 }}
        </span>
      </div>
    </div>

    <div v-if="stats" class="legend-stats">
      <div class="stat">
        <span class="stat-value">{{ stats.totalNodes }}</span>
        <span class="stat-label">Nodes</span>
      </div>
      <div class="stat">
        <span class="stat-value">{{ stats.totalEdges }}</span>
        <span class="stat-label">Edges</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.graph-legend {
  background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
  border: 1px solid #3d3d5c;
  border-radius: 10px;
  padding: 1rem;
}

.legend-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6a6a80;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #3d3d5c;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.legend-label {
  flex: 1;
  font-size: 0.85rem;
  color: #a0a0b0;
}

.legend-count {
  font-size: 0.85rem;
  font-weight: 600;
  color: #e0e0e0;
}

.legend-stats {
  display: flex;
  gap: 1.5rem;
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #e0e0e0;
}

.stat-label {
  font-size: 0.7rem;
  color: #6a6a80;
  text-transform: uppercase;
}
</style>

