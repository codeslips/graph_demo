<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  useMediaCrawlerStore,
  PLATFORM_OPTIONS,
  CRAWLER_TYPE_OPTIONS,
  LOGIN_TYPE_OPTIONS,
} from '@/stores/mediaCrawler'

const router = useRouter()
const store = useMediaCrawlerStore()

onMounted(async () => {
  await store.fetchStatus()
  
  // Start polling if already running
  if (store.isRunning) {
    store.startPolling()
  }
})

onUnmounted(() => {
  store.stopPolling()
})

async function handleSubmit() {
  await store.submitTask()
}

function goBack() {
  router.push('/media')
}
</script>

<template>
  <div class="crawl-task-view">
    <header class="view-header">
      <div class="header-content">
        <button class="btn-back" @click="goBack">
          ← 返回
        </button>
        <div class="title-section">
          <h1>媒体爬虫任务</h1>
          <p class="subtitle">配置并启动新的爬虫任务</p>
        </div>
      </div>
    </header>

    <!-- Service Unavailable Warning -->
    <div v-if="!store.serviceAvailable" class="warning-banner">
      <span class="warning-icon">⚠️</span>
      <span>无法连接到爬虫服务，请检查服务是否运行</span>
    </div>

    <!-- Error Message -->
    <div v-if="store.error" class="error-banner">
      <span class="error-icon">❌</span>
      <span>{{ store.error }}</span>
      <button class="dismiss-btn" @click="store.clearMessages">✕</button>
    </div>

    <!-- Success Message -->
    <div v-if="store.successMessage" class="success-banner">
      <span class="success-icon">✅</span>
      <span>{{ store.successMessage }}</span>
      <button class="dismiss-btn" @click="store.clearMessages">✕</button>
    </div>

    <div class="view-content">
      <!-- Current Status Card -->
      <div class="status-card">
        <h2 class="section-title">当前状态</h2>
        <div class="status-content">
          <div v-if="store.statusLoading" class="loading-status">
            <span class="spinner">⟳</span> 加载中...
          </div>
          <div v-else-if="store.isRunning" class="running-status">
            <div class="status-indicator running">
              <span class="status-dot"></span>
              运行中
            </div>
            <div class="status-details">
              <div class="detail-item">
                <span class="label">平台:</span>
                <span class="value">{{ store.crawlerStatus?.platform || '-' }}</span>
              </div>
              <div class="detail-item">
                <span class="label">类型:</span>
                <span class="value">{{ store.crawlerStatus?.crawler_type || '-' }}</span>
              </div>
              <div class="detail-item">
                <span class="label">开始时间:</span>
                <span class="value">{{ store.crawlerStatus?.started_at || '-' }}</span>
              </div>
            </div>
            <p class="running-message">
              ⏳ 任务正在执行中，请等待完成...
            </p>
          </div>
          <div v-else class="idle-status">
            <div class="status-indicator idle">
              <span class="status-dot"></span>
              空闲
            </div>
            <p class="idle-message">可以创建新的爬虫任务</p>
          </div>
        </div>
      </div>

      <!-- Task Form Card -->
      <div class="form-card" :class="{ disabled: !store.canSubmit }">
        <h2 class="section-title">任务配置</h2>
        
        <form class="task-form" @submit.prevent="handleSubmit">
          <!-- Platform Selection -->
          <div class="form-row">
            <div class="form-group">
              <label for="platform">平台 *</label>
              <select
                id="platform"
                v-model="store.formData.platform"
                :disabled="!store.canSubmit"
              >
                <option
                  v-for="option in PLATFORM_OPTIONS"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.icon }} {{ option.label }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="login_type">登录方式 *</label>
              <select
                id="login_type"
                v-model="store.formData.login_type"
                :disabled="!store.canSubmit"
              >
                <option
                  v-for="option in LOGIN_TYPE_OPTIONS"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="crawler_type">爬取类型 *</label>
              <select
                id="crawler_type"
                v-model="store.formData.crawler_type"
                :disabled="!store.canSubmit"
              >
                <option
                  v-for="option in CRAWLER_TYPE_OPTIONS"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </div>
          </div>

          <!-- Keywords and IDs -->
          <div class="form-row">
            <div class="form-group flex-2">
              <label for="keywords">搜索关键词</label>
              <input
                id="keywords"
                v-model="store.formData.keywords"
                type="text"
                placeholder="输入搜索关键词"
                :disabled="!store.canSubmit"
              />
            </div>
            
            <div class="form-group">
              <label for="start_page">起始页码</label>
              <input
                id="start_page"
                v-model.number="store.formData.start_page"
                type="number"
                min="1"
                :disabled="!store.canSubmit"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="specified_ids">指定内容ID</label>
              <input
                id="specified_ids"
                v-model="store.formData.specified_ids"
                type="text"
                placeholder="多个ID用逗号分隔"
                :disabled="!store.canSubmit"
              />
            </div>
            
            <div class="form-group">
              <label for="creator_ids">创作者ID</label>
              <input
                id="creator_ids"
                v-model="store.formData.creator_ids"
                type="text"
                placeholder="多个ID用逗号分隔"
                :disabled="!store.canSubmit"
              />
            </div>
          </div>

          <!-- Options -->
          <div class="form-row options-row">
            <div class="checkbox-group">
              <input
                id="enable_comments"
                v-model="store.formData.enable_comments"
                type="checkbox"
                :disabled="!store.canSubmit"
              />
              <label for="enable_comments">抓取评论</label>
            </div>
            
            <div class="checkbox-group">
              <input
                id="enable_sub_comments"
                v-model="store.formData.enable_sub_comments"
                type="checkbox"
                :disabled="!store.canSubmit"
              />
              <label for="enable_sub_comments">抓取子评论</label>
            </div>
            
            <div class="checkbox-group">
              <input
                id="headless"
                v-model="store.formData.headless"
                type="checkbox"
                :disabled="!store.canSubmit"
              />
              <label for="headless">无头模式</label>
            </div>
          </div>

          <!-- Cookies (optional) -->
          <div class="form-group">
            <label for="cookies">Cookies (可选)</label>
            <textarea
              id="cookies"
              v-model="store.formData.cookies"
              rows="3"
              placeholder="如使用Cookie登录，请在此粘贴Cookie字符串"
              :disabled="!store.canSubmit"
            ></textarea>
          </div>

          <!-- Submit Button -->
          <div class="form-actions">
            <button
              type="button"
              class="btn-reset"
              :disabled="!store.canSubmit"
              @click="store.resetForm"
            >
              重置
            </button>
            <button
              type="submit"
              class="btn-submit"
              :disabled="!store.canSubmit"
            >
              <span v-if="store.submitting" class="spinner">⟳</span>
              <span v-else>🚀</span>
              {{ store.submitting ? '启动中...' : '启动任务' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.crawl-task-view {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(180deg, #0a0a12 0%, #12121a 100%);
}

.view-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.btn-back {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #a0a0b0;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-back:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e0e0e0;
}

.title-section h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #e0e0e0;
  background: linear-gradient(135deg, #e0e0e0 0%, #a0a0b0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  margin: 0.25rem 0 0;
  color: #6a6a80;
  font-size: 0.9rem;
}

/* Banners */
.warning-banner,
.error-banner,
.success-banner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.warning-banner {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
  color: #fbbf24;
}

.error-banner {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
}

.success-banner {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #34d399;
}

.dismiss-btn {
  margin-left: auto;
  padding: 0.25rem 0.5rem;
  background: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.dismiss-btn:hover {
  opacity: 1;
}

/* Content */
.view-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 900px;
}

/* Cards */
.status-card,
.form-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 1.5rem;
}

.section-title {
  margin: 0 0 1.25rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #c0c0d0;
}

/* Status */
.loading-status {
  color: #6a6a80;
}

.spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-indicator.running {
  color: #fbbf24;
}

.status-indicator.running .status-dot {
  background: #fbbf24;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.status-indicator.idle {
  color: #34d399;
}

.status-indicator.idle .status-dot {
  background: #34d399;
}

.status-details {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item .label {
  font-size: 0.75rem;
  color: #6a6a80;
  text-transform: uppercase;
}

.detail-item .value {
  color: #e0e0e0;
  font-weight: 500;
}

.running-message,
.idle-message {
  margin-top: 1rem;
  color: #6a6a80;
  font-size: 0.9rem;
}

/* Form */
.form-card.disabled {
  opacity: 0.6;
  pointer-events: none;
}

.task-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.flex-2 {
  flex: 2;
}

.form-group label {
  font-size: 0.85rem;
  color: #a0a0b0;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem 1rem;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #e0e0e0;
  font-size: 0.9rem;
  transition: border-color 0.2s, background 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: rgba(99, 102, 241, 0.5);
  background: rgba(0, 0, 0, 0.4);
}

.form-group input:disabled,
.form-group select:disabled,
.form-group textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: #4a4a60;
}

.options-row {
  justify-content: flex-start;
  gap: 2rem;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #6366f1;
}

.checkbox-group label {
  color: #a0a0b0;
  font-size: 0.9rem;
  cursor: pointer;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 0.5rem;
}

.btn-reset,
.btn-submit {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reset {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #a0a0b0;
}

.btn-reset:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
}

.btn-submit {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-reset:disabled,
.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* Responsive */
@media (max-width: 768px) {
  .crawl-task-view {
    padding: 1rem;
  }
  
  .form-row {
    flex-direction: column;
  }
  
  .options-row {
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .status-details {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>

