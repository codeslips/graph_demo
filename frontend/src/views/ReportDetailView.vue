<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getReport } from '@/api/report'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import type { Report } from '@/types/report'

const route = useRoute()
const router = useRouter()

const report = ref<Report | null>(null)
const loading = ref(true)
const error = ref('')

const reportId = computed(() => route.params.id as string)

// Configure marked for safe rendering
marked.setOptions({
  breaks: true,
  gfm: true,
})

const renderedContent = computed(() => {
  if (!report.value?.content) return ''
  
  try {
    const html = marked(report.value.content) as string
    return DOMPurify.sanitize(html)
  } catch (e) {
    console.error('Failed to render markdown:', e)
    return report.value.content
  }
})

onMounted(async () => {
  await loadReport()
})

async function loadReport() {
  loading.value = true
  error.value = ''

  try {
    report.value = await getReport(reportId.value)
  } catch (e: any) {
    console.error('Failed to load report:', e)
    if (e.response?.status === 404) {
      error.value = '报告不存在'
    } else {
      error.value = e.message || '加载报告失败'
    }
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.push('/reports')
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

function formatTimestamp(ts: number | null | undefined): string {
  if (!ts) return '-'
  const date = new Date(ts * 1000)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}

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
</script>

<template>
  <div class="report-detail-view">
    <!-- Header -->
    <header class="view-header">
      <button class="back-btn" @click="goBack">
        ← 返回列表
      </button>
    </header>

    <!-- Loading state -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">❌</div>
      <h3>加载失败</h3>
      <p>{{ error }}</p>
      <button class="btn-primary" @click="goBack">返回列表</button>
    </div>

    <!-- Report content -->
    <div v-else-if="report" class="report-container">
      <!-- Report header -->
      <div class="report-header">
        <h1>{{ report.title }}</h1>
        <div class="report-meta">
          <span class="meta-item platform">
            <span class="meta-icon">📱</span>
            {{ getPlatformLabel(report.platform) }}
          </span>
          <span class="meta-item keyword">
            <span class="meta-icon">🔍</span>
            {{ report.source_keyword }}
          </span>
          <span class="meta-item records">
            <span class="meta-icon">📝</span>
            {{ report.record_count }} 条记录
          </span>
        </div>
        <div class="report-time-info">
          <span v-if="report.time_from || report.time_to" class="time-range">
            📅 数据范围: {{ formatTimestamp(report.time_from) }} - {{ formatTimestamp(report.time_to) }}
          </span>
          <span class="created-at">
            🕐 创建于 {{ formatDate(report.created_at) }}
          </span>
        </div>
      </div>

      <!-- Report content -->
      <div class="report-content">
        <div class="content-wrapper" v-html="renderedContent"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.report-detail-view {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(180deg, #0a0a12 0%, #12121a 100%);
}

.view-header {
  margin-bottom: 2rem;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 8px;
  color: #a78bfa;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: rgba(99, 102, 241, 0.2);
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(99, 102, 241, 0.2);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p,
.error-state p {
  color: #6a6a80;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-state h3 {
  margin: 0 0 0.5rem;
  color: #f87171;
}

.btn-primary {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
}

.report-container {
  max-width: 900px;
  margin: 0 auto;
}

.report-header {
  background: rgba(30, 30, 46, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.report-header h1 {
  margin: 0 0 1.25rem;
  font-size: 1.75rem;
  font-weight: 700;
  color: #e0e0e0;
  background: linear-gradient(135deg, #e0e0e0 0%, #60a5fa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.report-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background: rgba(10, 10, 18, 0.5);
}

.meta-icon {
  font-size: 1rem;
}

.meta-item.platform {
  color: #60a5fa;
  border: 1px solid rgba(96, 165, 250, 0.3);
}

.meta-item.keyword {
  color: #a78bfa;
  border: 1px solid rgba(167, 139, 250, 0.3);
}

.meta-item.records {
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.report-time-info {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  font-size: 0.9rem;
  color: #6a6a80;
}

.time-range,
.created-at {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.report-content {
  background: rgba(30, 30, 46, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 16px;
  padding: 2rem;
}

.content-wrapper {
  color: #d0d0d0;
  font-size: 1rem;
  line-height: 1.8;
}

/* Markdown content styling */
.content-wrapper :deep(h1),
.content-wrapper :deep(h2),
.content-wrapper :deep(h3),
.content-wrapper :deep(h4),
.content-wrapper :deep(h5),
.content-wrapper :deep(h6) {
  color: #e0e0e0;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.content-wrapper :deep(h1) { font-size: 1.75rem; }
.content-wrapper :deep(h2) { font-size: 1.5rem; }
.content-wrapper :deep(h3) { font-size: 1.25rem; }
.content-wrapper :deep(h4) { font-size: 1.1rem; }

.content-wrapper :deep(p) {
  margin: 1em 0;
}

.content-wrapper :deep(ul),
.content-wrapper :deep(ol) {
  margin: 1em 0;
  padding-left: 2em;
}

.content-wrapper :deep(li) {
  margin: 0.5em 0;
}

.content-wrapper :deep(strong) {
  color: #e0e0e0;
  font-weight: 600;
}

.content-wrapper :deep(em) {
  color: #a78bfa;
}

.content-wrapper :deep(code) {
  background: rgba(99, 102, 241, 0.15);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-family: 'Fira Code', 'Monaco', monospace;
  font-size: 0.9em;
  color: #a78bfa;
}

.content-wrapper :deep(pre) {
  background: rgba(10, 10, 18, 0.8);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 8px;
  padding: 1rem;
  overflow-x: auto;
  margin: 1em 0;
}

.content-wrapper :deep(pre code) {
  background: transparent;
  padding: 0;
}

.content-wrapper :deep(blockquote) {
  border-left: 4px solid #6366f1;
  margin: 1em 0;
  padding: 0.5em 1em;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 0 8px 8px 0;
}

.content-wrapper :deep(hr) {
  border: none;
  border-top: 1px solid rgba(99, 102, 241, 0.2);
  margin: 2em 0;
}

.content-wrapper :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
}

.content-wrapper :deep(th),
.content-wrapper :deep(td) {
  border: 1px solid rgba(99, 102, 241, 0.2);
  padding: 0.75em 1em;
  text-align: left;
}

.content-wrapper :deep(th) {
  background: rgba(99, 102, 241, 0.1);
  color: #e0e0e0;
  font-weight: 600;
}

.content-wrapper :deep(tr:nth-child(even)) {
  background: rgba(10, 10, 18, 0.3);
}

.content-wrapper :deep(a) {
  color: #60a5fa;
  text-decoration: none;
}

.content-wrapper :deep(a:hover) {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .report-detail-view {
    padding: 1rem;
  }

  .report-header,
  .report-content {
    padding: 1.25rem;
  }

  .report-meta {
    flex-direction: column;
    gap: 0.75rem;
  }

  .report-time-info {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>

