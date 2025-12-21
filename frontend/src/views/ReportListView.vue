<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getReports, deleteReport } from '@/api/report'
import type { ReportListItem } from '@/types/report'

const router = useRouter()

const reports = ref<ReportListItem[]>([])
const total = ref(0)
const loading = ref(false)
const error = ref('')
const currentPage = ref(1)
const pageSize = 20

// Delete confirmation
const showDeleteModal = ref(false)
const deletingId = ref<string | null>(null)
const deleting = ref(false)

const totalPages = computed(() => Math.ceil(total.value / pageSize))

onMounted(() => {
  loadReports()
})

async function loadReports() {
  loading.value = true
  error.value = ''
  
  try {
    const offset = (currentPage.value - 1) * pageSize
    const response = await getReports(pageSize, offset)
    reports.value = response.items
    total.value = response.total
  } catch (e: any) {
    console.error('Failed to load reports:', e)
    error.value = e.message || '加载报告列表失败'
  } finally {
    loading.value = false
  }
}

function goToDetail(id: string) {
  router.push(`/reports/${id}`)
}

function confirmDelete(id: string) {
  deletingId.value = id
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!deletingId.value) return

  deleting.value = true
  try {
    await deleteReport(deletingId.value)
    showDeleteModal.value = false
    deletingId.value = null
    await loadReports()
  } catch (e: any) {
    console.error('Failed to delete report:', e)
    error.value = e.message || '删除失败'
  } finally {
    deleting.value = false
  }
}

function cancelDelete() {
  showDeleteModal.value = false
  deletingId.value = null
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    loadReports()
  }
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    loadReports()
  }
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatTimestamp(ts: number | null | undefined): string {
  if (!ts) return '-'
  const date = new Date(ts * 1000)
  return date.toLocaleDateString('zh-CN')
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
  <div class="report-list-view">
    <header class="view-header">
      <div class="header-content">
        <h1>📊 分析报告</h1>
        <p class="subtitle">查看已保存的分析报告</p>
      </div>
    </header>

    <!-- Error display -->
    <div v-if="error" class="error-banner">
      <span class="error-icon">❌</span>
      <span>{{ error }}</span>
      <button class="dismiss-btn" @click="error = ''">✕</button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="reports.length === 0" class="empty-state">
      <div class="empty-icon">📋</div>
      <h3>暂无报告</h3>
      <p>前往媒体数据页面生成分析报告</p>
      <button class="btn-primary" @click="router.push('/media')">
        去生成报告
      </button>
    </div>

    <!-- Report list -->
    <div v-else class="report-list">
      <div
        v-for="report in reports"
        :key="report.id"
        class="report-card"
        @click="goToDetail(report.id)"
      >
        <div class="card-content">
          <h3 class="report-title">{{ report.title }}</h3>
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
            <span v-if="report.time_from || report.time_to" class="meta-item time-range">
              <span class="meta-icon">📅</span>
              {{ formatTimestamp(report.time_from) }} - {{ formatTimestamp(report.time_to) }}
            </span>
          </div>
          <div class="report-date">
            创建于 {{ formatDate(report.created_at) }}
          </div>
        </div>
        <div class="card-actions" @click.stop>
          <button class="btn-delete" @click="confirmDelete(report.id)">
            🗑️
          </button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button
        class="page-btn"
        :disabled="currentPage === 1"
        @click="prevPage"
      >
        ← 上一页
      </button>
      <span class="page-info">
        第 {{ currentPage }} / {{ totalPages }} 页
      </span>
      <button
        class="page-btn"
        :disabled="currentPage === totalPages"
        @click="nextPage"
      >
        下一页 →
      </button>
    </div>

    <!-- Delete confirmation modal -->
    <Teleport to="body">
      <div v-if="showDeleteModal" class="modal-backdrop" @click="cancelDelete">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>确认删除</h3>
          </div>
          <div class="modal-body">
            <p>确定要删除这份报告吗？此操作无法撤销。</p>
          </div>
          <div class="modal-footer">
            <button class="btn-cancel" @click="cancelDelete">取消</button>
            <button
              class="btn-confirm-delete"
              :disabled="deleting"
              @click="handleDelete"
            >
              {{ deleting ? '删除中...' : '确认删除' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.report-list-view {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(180deg, #0a0a12 0%, #12121a 100%);
}

.view-header {
  margin-bottom: 2rem;
}

.header-content h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #e0e0e0;
  background: linear-gradient(135deg, #e0e0e0 0%, #60a5fa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  margin: 0.25rem 0 0;
  color: #6a6a80;
  font-size: 0.9rem;
}

.error-banner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
}

.error-icon {
  font-size: 1.25rem;
}

.dismiss-btn {
  margin-left: auto;
  padding: 0.25rem 0.5rem;
  background: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
  opacity: 0.7;
}

.dismiss-btn:hover {
  opacity: 1;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: #6a6a80;
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  color: #c0c0c0;
}

.empty-state p {
  margin: 0 0 1.5rem;
  color: #6a6a80;
}

.btn-primary {
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

.report-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.report-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background: rgba(30, 30, 46, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.report-card:hover {
  background: rgba(30, 30, 46, 0.8);
  border-color: rgba(99, 102, 241, 0.3);
  transform: translateY(-2px);
}

.card-content {
  flex: 1;
}

.report-title {
  margin: 0 0 0.75rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #e0e0e0;
}

.report-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.85rem;
  color: #a0a0b0;
}

.meta-icon {
  font-size: 0.9rem;
}

.meta-item.platform {
  color: #60a5fa;
}

.meta-item.keyword {
  color: #a78bfa;
}

.meta-item.records {
  color: #10b981;
}

.meta-item.time-range {
  color: #fbbf24;
}

.report-date {
  font-size: 0.8rem;
  color: #6a6a80;
}

.card-actions {
  flex-shrink: 0;
  margin-left: 1rem;
}

.btn-delete {
  padding: 0.5rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 6px;
  color: #f87171;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.2);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-btn {
  padding: 0.625rem 1rem;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 6px;
  color: #a78bfa;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: rgba(99, 102, 241, 0.2);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9rem;
  color: #a0a0b0;
}

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.modal-content {
  background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  overflow: hidden;
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(99, 102, 241, 0.15);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #e0e0e0;
}

.modal-body {
  padding: 1.5rem;
}

.modal-body p {
  margin: 0;
  color: #a0a0b0;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(99, 102, 241, 0.15);
}

.btn-cancel,
.btn-confirm-delete {
  padding: 0.625rem 1.25rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: transparent;
  border: 1px solid rgba(99, 102, 241, 0.2);
  color: #a0a0b0;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.05);
}

.btn-confirm-delete {
  background: rgba(239, 68, 68, 0.9);
  border: none;
  color: white;
}

.btn-confirm-delete:hover:not(:disabled) {
  background: #ef4444;
}

.btn-confirm-delete:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .report-list-view {
    padding: 1rem;
  }

  .report-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .card-actions {
    margin-left: 0;
    align-self: flex-end;
  }

  .report-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>

