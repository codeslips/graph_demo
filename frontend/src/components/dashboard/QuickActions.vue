<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const actions = [
  {
    id: 'crawl',
    icon: '🕷️',
    label: '启动爬虫任务',
    route: '/media/crawl',
    color: '#f59e0b',
  },
  {
    id: 'data',
    icon: '📊',
    label: '查看媒体数据',
    route: '/media',
    color: '#6366f1',
  },
  {
    id: 'reports',
    icon: '📋',
    label: '查看分析报告',
    route: '/reports',
    color: '#10b981',
  },
  {
    id: 'graph',
    icon: '🕸️',
    label: '探索知识图谱',
    route: '/media-graph',
    color: '#8b5cf6',
  },
  {
    id: 'chat',
    icon: '🤖',
    label: 'AI 对话分析',
    route: '/chat',
    color: '#ec4899',
  },
  {
    id: 'tech',
    icon: '⚙️',
    label: '架构技术栈',
    route: '/tech-stack',
    color: '#94a3b8',
  },
]

function goTo(route: string) {
  router.push(route)
}
</script>

<template>
  <div class="quick-actions">
    <h2 class="section-title">快捷操作</h2>
    
    <div class="actions-grid">
      <button
        v-for="action in actions"
        :key="action.id"
        class="action-btn"
        :style="{ '--action-color': action.color }"
        @click="goTo(action.route)"
      >
        <span class="action-icon">{{ action.icon }}</span>
        <span class="action-label">{{ action.label }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.quick-actions {
  padding: 0;
}

.section-title {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 700;
  color: #f1f5f9;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 0.75rem;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.01);
  border: 1px solid rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  color: #e2e8f0;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.action-btn:hover {
  background: color-mix(in srgb, var(--action-color) 10%, rgba(255, 255, 255, 0.01));
  border-color: var(--action-color);
  transform: translateY(-2px);
  color: #fff;
}

.action-icon {
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.action-btn:hover .action-icon {
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .actions-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }

  .action-btn {
    justify-content: center;
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>

