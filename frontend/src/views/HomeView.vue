<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useDashboard } from '@/composables/useDashboard'
import DashboardStats from '@/components/dashboard/DashboardStats.vue'
import WorkflowGuide from '@/components/dashboard/WorkflowGuide.vue'
import QuickActions from '@/components/dashboard/QuickActions.vue'
import RecentActivity from '@/components/dashboard/RecentActivity.vue'
import FeatureCards from '@/components/dashboard/FeatureCards.vue'

const router = useRouter()
const { stats, recentReports, loading, error, refresh } = useDashboard()
</script>

<template>
  <div class="home-view">
    <!-- Header Section -->
    <header class="dashboard-header">
      <div class="header-content">
        <h1 class="title">
          <span class="gradient-text">旅游分析平台</span>
        </h1>
        <p class="subtitle">
          多平台媒体数据采集、智能分析与知识图谱可视化
        </p>
      </div>
      <button class="refresh-btn" :disabled="loading" @click="refresh">
        <span class="refresh-icon" :class="{ spinning: loading }">⟳</span>
        刷新数据
      </button>
    </header>

    <!-- Error Banner -->
    <div v-if="error" class="error-banner">
      <span class="error-icon">⚠️</span>
      <span>{{ error }}</span>
      <button class="dismiss-btn" @click="error = null">✕</button>
    </div>

    <!-- Statistics Cards -->
    <section class="stats-section">
      <DashboardStats :stats="stats" :loading="loading" />
    </section>

    <!-- Main Content: Workspace area (Workflow + Quick Actions) + Activity Side -->
    <main class="dashboard-main">
      <div class="workspace-area">
        <section class="workflow-card">
          <WorkflowGuide />
        </section>
        
        <section class="quick-actions-card">
          <QuickActions />
        </section>
      </div>

      <aside class="activity-area">
        <RecentActivity
          :reports="recentReports"
          :crawler-status="stats.crawlerStatus"
          :loading="loading"
        />
      </aside>
    </main>

    <!-- Feature Cards -->
    <section class="features-section">
      <FeatureCards />
    </section>

    <!-- Tech Stack Footer -->
    <footer class="tech-stack">
      <div class="tech-grid" @click="router.push('/tech-stack')" style="cursor: pointer">
        <span class="tech-tag">Django Ninja</span>
        <span class="tech-tag">Vue 3 + TS</span>
        <span class="tech-tag">Neo4j</span>
        <span class="tech-tag">Celery</span>
        <span class="tech-tag">Coze AI</span>
        <span class="tech-tag more">查看完整架构 →</span>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.home-view {
  min-height: calc(100vh - 60px);
  padding: 1.5rem 2rem;
  background: 
    radial-gradient(circle at 0% 0%, rgba(99, 102, 241, 0.05) 0%, transparent 30%),
    radial-gradient(circle at 100% 100%, rgba(139, 92, 246, 0.05) 0%, transparent 30%),
    #0a0a0f;
  color: #e2e8f0;
}

/* Header */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.title {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  margin: 0;
}

.gradient-text {
  background: linear-gradient(135deg, #fff 0%, #a5b4fc 50%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 0.875rem;
  color: #94a3b8;
  font-weight: 400;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #94a3b8;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(8px);
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.06);
  border-color: #6366f1;
  color: #fff;
  transform: translateY(-1px);
}

.refresh-icon {
  font-size: 1rem;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Error Banner */
.error-banner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  color: #fca5a5;
  font-size: 0.875rem;
  margin-bottom: 1.5rem;
}

/* Dashboard Main Grid */
.dashboard-main {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.workspace-area {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.workflow-card, .quick-actions-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 1.25rem;
  backdrop-filter: blur(12px);
}

.activity-area {
  display: flex;
  flex-direction: column;
}

/* Sections */
.stats-section {
  margin-bottom: 0.5rem;
}

.features-section {
  margin-top: 2rem;
  margin-bottom: 3rem;
}

/* Tech Stack Footer */
.tech-stack {
  padding: 2rem 0;
  text-align: center;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.tech-grid {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.tech-tag {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.03);
  transition: all 0.2s ease;
}

.tech-grid:hover .tech-tag.more {
  color: #818cf8;
  border-color: rgba(99, 102, 241, 0.3);
  background: rgba(99, 102, 241, 0.05);
}

/* Responsive */
@media (max-width: 1200px) {
  .dashboard-main {
    grid-template-columns: 1fr;
  }
  
  .activity-area {
    order: 3;
  }
}

@media (max-width: 768px) {
  .home-view {
    padding: 1rem;
  }

  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .title {
    font-size: 1.5rem;
  }
}
</style>
