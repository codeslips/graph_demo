<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const steps = [
  {
    id: 1,
    icon: '🕷️',
    title: '启动爬虫',
    description: '配置并启动媒体数据爬取任务',
    route: '/media/crawl',
  },
  {
    id: 2,
    icon: '📊',
    title: '管理数据',
    description: '查看、筛选和管理爬取的媒体数据',
    route: '/media',
  },
  {
    id: 3,
    icon: '📋',
    title: '生成报告',
    description: '使用 AI 分析数据并生成洞察报告',
    route: '/reports',
  },
  {
    id: 4,
    icon: '🕸️',
    title: '探索图谱',
    description: '可视化探索数据之间的关系网络',
    route: '/media-graph',
  },
]

function goToStep(route: string) {
  router.push(route)
}
</script>

<template>
  <div class="workflow-section">
    <h2 class="section-title">快速开始</h2>
    <p class="section-desc">按照以下步骤使用平台</p>
    
    <div class="workflow-steps">
      <div
        v-for="(step, index) in steps"
        :key="step.id"
        class="step-item"
        @click="goToStep(step.route)"
      >
        <div class="step-number">{{ step.id }}</div>
        <div class="step-icon">{{ step.icon }}</div>
        <div class="step-content">
          <h3 class="step-title">{{ step.title }}</h3>
          <p class="step-desc">{{ step.description }}</p>
        </div>
        <div v-if="index < steps.length - 1" class="step-arrow">→</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.workflow-section {
  padding: 0;
}

.section-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #f1f5f9;
}

.section-desc {
  margin: 0.25rem 0 1.25rem;
  color: #64748b;
  font-size: 0.8125rem;
}

.workflow-steps {
  display: flex;
  align-items: stretch;
  gap: 0.75rem;
}

.step-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1rem 0.75rem;
  background: rgba(255, 255, 255, 0.01);
  border: 1px solid rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.step-item:hover {
  background: rgba(99, 102, 241, 0.05);
  border-color: rgba(99, 102, 241, 0.2);
  transform: translateY(-2px);
}

.step-number {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
  font-size: 0.625rem;
  font-weight: 700;
  color: #94a3b8;
}

.step-item:hover .step-number {
  background: #6366f1;
  color: white;
}

.step-icon {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
}

.step-content {
  flex: 1;
}

.step-title {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #e2e8f0;
}

.step-desc {
  margin: 0.25rem 0 0;
  font-size: 0.75rem;
  color: #94a3b8;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.step-arrow {
  display: none;
}

@media (max-width: 1024px) {
  .workflow-steps {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .step-arrow {
    display: none;
  }
}

@media (max-width: 640px) {
  .workflow-steps {
    grid-template-columns: 1fr;
  }

  .step-item {
    flex-direction: row;
    text-align: left;
    gap: 1rem;
    padding: 1rem 1.25rem;
  }

  .step-number {
    position: static;
    transform: none;
    flex-shrink: 0;
  }

  .step-icon {
    font-size: 2rem;
    margin-bottom: 0;
    flex-shrink: 0;
  }
}
</style>

