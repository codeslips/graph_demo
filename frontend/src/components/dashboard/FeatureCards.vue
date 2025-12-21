<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const features = [
  {
    id: 'crawler',
    icon: '🕷️',
    title: '媒体爬虫',
    description: '支持小红书、抖音、微博等多平台数据采集',
    route: '/media/crawl',
    color: '#f59e0b',
  },
  {
    id: 'data',
    icon: '📊',
    title: '数据管理',
    description: '统一管理各平台爬取的媒体数据',
    route: '/media',
    color: '#6366f1',
  },
  {
    id: 'reports',
    icon: '📋',
    title: '分析报告',
    description: 'AI 驱动的数据分析与洞察生成',
    route: '/reports',
    color: '#10b981',
  },
  {
    id: 'graph',
    icon: '🕸️',
    title: '知识图谱',
    description: '可视化探索数据间的关系网络',
    route: '/media-graph',
    color: '#8b5cf6',
  },
  {
    id: 'chat',
    icon: '🤖',
    title: 'AI 对话',
    description: '与 AI 助手对话分析数据',
    route: '/chat',
    color: '#ec4899',
  },
]

function goTo(route: string) {
  router.push(route)
}
</script>

<template>
  <div class="features-section">
    <h2 class="section-title">功能模块</h2>
    
    <div class="features-grid">
      <div
        v-for="feature in features"
        :key="feature.id"
        class="feature-card"
        :style="{ '--card-color': feature.color }"
        @click="goTo(feature.route)"
      >
        <div class="feature-icon">{{ feature.icon }}</div>
        <div class="feature-content">
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-desc">{{ feature.description }}</p>
        </div>
        <div class="feature-action">
          <span class="action-text">进入</span>
          <span class="action-arrow">→</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.features-section {
  padding: 0;
}

.section-title {
  margin: 0 0 1.25rem;
  font-size: 1.125rem;
  font-weight: 700;
  color: #f1f5f9;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem;
}

.feature-card {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--card-color), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-6px);
  box-shadow: 0 20px 40px -20px rgba(0, 0, 0, 0.5);
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1.25rem;
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  filter: drop-shadow(0 0 8px rgba(0,0,0,0.3));
}

.feature-card:hover .feature-icon {
  transform: scale(1.1) rotate(5deg);
}

.feature-content {
  flex: 1;
  margin-bottom: 1.5rem;
}

.feature-title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 700;
  color: #f8fafc;
}

.feature-desc {
  margin: 0.5rem 0 0;
  font-size: 0.875rem;
  color: #94a3b8;
  line-height: 1.6;
}

.feature-action {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.8125rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: all 0.3s ease;
}

.feature-card:hover .feature-action {
  color: var(--card-color);
}

.action-arrow {
  transition: transform 0.3s ease;
}

.feature-card:hover .action-arrow {
  transform: translateX(6px);
}

@media (max-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .features-grid {
    grid-template-columns: 1fr;
  }

  .feature-card {
    padding: 1.25rem;
  }
}
</style>

