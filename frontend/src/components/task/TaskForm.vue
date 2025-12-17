<script setup lang="ts">
import { ref } from 'vue'
import type { CrawlType } from '@/types/crawl'

const emit = defineEmits<{
  submit: [data: { target_url: string; crawl_type: CrawlType }]
}>()

const targetUrl = ref('https://www.thepaper.cn/channel_25953')
const crawlType = ref<CrawlType>('news_list')
const isSubmitting = ref(false)

    const crawlTypes: { value: CrawlType; label: string }[] = [
  { value: 'news_list', label: '新闻列表 (多篇文章)' },
  { value: 'article', label: '单篇文章' },
  { value: 'channel', label: '完整频道' }
]

async function handleSubmit() {
  if (!targetUrl.value.trim()) return

  isSubmitting.value = true
  try {
    emit('submit', {
      target_url: targetUrl.value.trim(),
      crawl_type: crawlType.value
    })
    // Reset form
    targetUrl.value = 'https://www.thepaper.cn/channel_25953'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <form class="task-form" @submit.prevent="handleSubmit">
    <h3 class="form-title">创建新爬取任务</h3>

    <div class="form-group">
      <label for="target-url">目标 URL</label>
      <input
        id="target-url"
        v-model="targetUrl"
        type="url"
        placeholder="https://www.thepaper.cn/channel_25953"
        required
        :disabled="isSubmitting"
      />
      <span class="hint">输入澎湃新闻频道或文章 URL</span>
    </div>

    <div class="form-group">
      <label for="crawl-type">爬取类型</label>
      <select id="crawl-type" v-model="crawlType" :disabled="isSubmitting">
        <option v-for="type in crawlTypes" :key="type.value" :value="type.value">
          {{ type.label }}
        </option>
      </select>
    </div>

    <button type="submit" class="submit-btn" :disabled="isSubmitting || !targetUrl.trim()">
      <span v-if="isSubmitting" class="spinner"></span>
      {{ isSubmitting ? '启动中...' : '开始爬取' }}
    </button>
  </form>
</template>

<style scoped>
.task-form {
  background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
  border: 1px solid #3d3d5c;
  border-radius: 12px;
  padding: 1.5rem;
}

.form-title {
  margin: 0 0 1.25rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #e0e0e0;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.4rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #a0a0b0;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.625rem 0.875rem;
  background: #12121a;
  border: 1px solid #3d3d5c;
  border-radius: 8px;
  color: #e0e0e0;
  font-size: 0.9rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.form-group input::placeholder {
  color: #5a5a70;
}

.hint {
  display: block;
  margin-top: 0.3rem;
  font-size: 0.75rem;
  color: #6a6a80;
}

.submit-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
}

.submit-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.submit-btn:active:not(:disabled) {
  transform: scale(0.98);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>

