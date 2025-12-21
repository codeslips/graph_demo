<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { RecentReport } from '@/types/dashboard'

defineProps<{
  reports: RecentReport[]
  crawlerStatus: 'running' | 'idle'
  loading: boolean
}>()

const router = useRouter()

const platformLabels: Record<string, string> = {
  xhs: '小红书',
  douyin: '抖音',
  weibo: '微博',
  bilibili: 'B站',
  kuaishou: '快手',
  tieba: '贴吧',
  zhihu: '知乎',
}

function getPlatformLabel(platform: string): string {
  return platformLabels[platform] || platform
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function goToReport(id: string) {
  router.push(`/reports/${id}`)
}

function goToReports() {
  router.push('/reports')
}

function goToCrawler() {
  router.push('/media/crawl')
}
</script>

<template>
  <div class="recent-activity">
    <h2 class="section-title">最近动态</h2>
    
    <!-- Crawler Status -->
    <div class="activity-card crawler-status" @click="goToCrawler">
      <div class="status-header">
        <span class="status-icon">🕷️</span>
        <span class="status-title">爬虫状态</span>
      </div>
      <div class="status-content">
        <span 
          class="status-badge"
          :class="crawlerStatus === 'running' ? 'running' : 'idle'"
        >
          <span class="status-dot"></span>
          {{ crawlerStatus === 'running' ? '运行中' : '空闲' }}
        </span>
        <span class="status-action">查看详情 →</span>
      </div>
    </div>

    <!-- Recent Reports -->
    <div class="reports-section">
      <div class="reports-header">
        <span class="reports-icon">📋</span>
        <span class="reports-title">最近报告</span>
        <button v-if="reports.length > 0" class="view-all-btn" @click="goToReports">
          查看全部 →
        </button>
      </div>

      <div v-if="loading" class="loading-state">
        <div v-for="i in 3" :key="i" class="skeleton-item">
          <div class="skeleton skeleton-title"></div>
          <div class="skeleton skeleton-meta"></div>
        </div>
      </div>

      <div v-else-if="reports.length === 0" class="empty-state">
        <span class="empty-icon">📭</span>
        <p>暂无分析报告</p>
        <button class="create-btn" @click="router.push('/media')">
          去生成报告
        </button>
      </div>

      <div v-else class="reports-list">
        <div
          v-for="report in reports"
          :key="report.id"
          class="report-item"
          @click="goToReport(report.id)"
        >
          <div class="report-info">
            <span class="report-title">{{ report.title }}</span>
            <span class="report-meta">
              <span class="platform-tag">{{ getPlatformLabel(report.platform) }}</span>
              <span class="report-date">{{ formatDate(report.createdAt) }}</span>
            </span>
          </div>
          <span class="report-arrow">→</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recent-activity {
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.section-title {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 700;
  color: #f1f5f9;
}

.activity-card {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(8px);
}

.activity-card:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(99, 102, 241, 0.3);
  transform: translateX(4px);
}

.status-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.status-icon {
  font-size: 1rem;
}

.status-title {
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 700;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-badge.running {
  color: #fbbf24;
}

.status-badge.running .status-dot {
  background: #fbbf24;
  box-shadow: 0 0 10px #fbbf24;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.status-badge.idle {
  color: #10b981;
}

.status-badge.idle .status-dot {
  background: #10b981;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(1.5); }
}

.status-action {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

/* Reports Section */
.reports-section {
  flex: 1;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.reports-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.01);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.reports-icon {
  font-size: 1rem;
}

.reports-title {
  font-size: 0.875rem;
  color: #e2e8f0;
  font-weight: 600;
  flex: 1;
}

.view-all-btn {
  background: none;
  border: none;
  color: #6366f1;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.view-all-btn:hover {
  color: #818cf8;
  transform: translateX(2px);
}

.reports-list {
  padding: 0.25rem 0;
  overflow-y: auto;
}

.report-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.875rem 1.25rem;
  cursor: pointer;
  transition: all 0.2s;
  border-bottom: 1px solid rgba(255, 255, 255, 0.02);
}

.report-item:last-child {
  border-bottom: none;
}

.report-item:hover {
  background: rgba(99, 102, 241, 0.05);
}

.report-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.report-title {
  font-size: 0.875rem;
  color: #f1f5f9;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.report-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.75rem;
}

.platform-tag {
  color: #818cf8;
  font-weight: 600;
}

.report-date {
  color: #64748b;
}

.report-arrow {
  color: #475569;
  font-size: 0.875rem;
  transition: transform 0.2s;
}

.report-item:hover .report-arrow {
  color: #6366f1;
  transform: translateX(4px);
}

.empty-state {
  padding: 2.5rem 1.25rem;
  text-align: center;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  opacity: 0.5;
}

.empty-state p {
  margin: 0 0 1rem;
  color: #64748b;
  font-size: 0.8125rem;
}
</style>

