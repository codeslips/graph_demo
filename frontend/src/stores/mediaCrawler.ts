/**
 * Media Crawler Pinia Store
 * Manages state for crawler task management
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { startCrawlerTask, getCrawlerStatus } from '@/api/mediaCrawler'
import type {
  CrawlerPlatform,
  LoginType,
  CrawlerType,
  CrawlerStartRequest,
  CrawlerStatusResponse,
  PlatformOption,
  CrawlerTypeOption,
  LoginTypeOption,
} from '@/types/mediaCrawler'

// Platform options
export const PLATFORM_OPTIONS: PlatformOption[] = [
  { value: 'xhs', label: '小红书', icon: '📕' },
  { value: 'douyin', label: '抖音', icon: '🎵' },
  { value: 'bilibili', label: 'Bilibili', icon: '📺' },
  { value: 'kuaishou', label: '快手', icon: '🎬' },
  { value: 'weibo', label: '微博', icon: '📱' },
  { value: 'tieba', label: '贴吧', icon: '💬' },
  { value: 'zhihu', label: '知乎', icon: '📖' },
]

// Crawler type options
export const CRAWLER_TYPE_OPTIONS: CrawlerTypeOption[] = [
  { value: 'search', label: '搜索' },
  { value: 'detail', label: '详情' },
  { value: 'creator', label: '创作者' },
]

// Login type options
export const LOGIN_TYPE_OPTIONS: LoginTypeOption[] = [
  { value: 'qrcode', label: '扫码登录' },
  { value: 'cookie', label: 'Cookie登录' },
]

export const useMediaCrawlerStore = defineStore('mediaCrawler', () => {
  // State
  const loading = ref(false)
  const submitting = ref(false)
  const error = ref<string | null>(null)
  const successMessage = ref<string | null>(null)
  
  // Crawler status
  const crawlerStatus = ref<CrawlerStatusResponse | null>(null)
  const statusLoading = ref(false)
  const serviceAvailable = ref(true)
  
  // Form state
  const formData = ref<CrawlerStartRequest>({
    platform: 'xhs',
    login_type: 'qrcode',
    crawler_type: 'search',
    keywords: '',
    specified_ids: '',
    creator_ids: '',
    start_page: 1,
    enable_comments: true,
    enable_sub_comments: false,
    save_option: 'db',
    cookies: '',
    headless: false,
  })
  
  // Polling
  let pollInterval: ReturnType<typeof setInterval> | null = null

  // Computed
  const isRunning = computed(() => crawlerStatus.value?.status === 'running')
  const isIdle = computed(() => crawlerStatus.value?.status === 'idle')
  const canSubmit = computed(() => 
    !isRunning.value && !submitting.value && serviceAvailable.value
  )

  // Actions
  async function fetchStatus() {
    statusLoading.value = true
    error.value = null
    
    try {
      crawlerStatus.value = await getCrawlerStatus()
      serviceAvailable.value = true
    } catch (e: any) {
      serviceAvailable.value = false
      if (e.response?.data?.detail) {
        error.value = e.response.data.detail
      } else {
        error.value = '无法连接到爬虫服务'
      }
    } finally {
      statusLoading.value = false
    }
  }

  async function submitTask() {
    if (!canSubmit.value) return false
    
    submitting.value = true
    error.value = null
    successMessage.value = null
    
    try {
      // First check current status
      await fetchStatus()
      
      if (isRunning.value) {
        error.value = '当前有任务正在运行，请等待完成后再创建新任务'
        return false
      }
      
      // Start the task
      const response = await startCrawlerTask(formData.value)
      
      if (response.success) {
        successMessage.value = response.message || '爬虫任务已启动'
        // Start polling for status
        startPolling()
        return true
      } else {
        error.value = response.message || '启动任务失败'
        return false
      }
    } catch (e: any) {
      if (e.response?.data?.detail) {
        error.value = e.response.data.detail
      } else {
        error.value = e.message || '启动任务失败'
      }
      return false
    } finally {
      submitting.value = false
    }
  }

  function startPolling() {
    stopPolling()
    
    pollInterval = setInterval(async () => {
      const wasRunning = isRunning.value
      await fetchStatus()
      
      // Check if task just completed
      if (wasRunning && isIdle.value) {
        stopPolling()
        
        if (crawlerStatus.value?.error_message) {
          error.value = `任务失败: ${crawlerStatus.value.error_message}`
        } else {
          successMessage.value = '爬虫任务已完成!'
          setTimeout(() => {
            successMessage.value = null
          }, 5000)
        }
      }
    }, 3000) // Poll every 3 seconds
  }

  function stopPolling() {
    if (pollInterval) {
      clearInterval(pollInterval)
      pollInterval = null
    }
  }

  function resetForm() {
    formData.value = {
      platform: 'xhs',
      login_type: 'qrcode',
      crawler_type: 'search',
      keywords: '',
      specified_ids: '',
      creator_ids: '',
      start_page: 1,
      enable_comments: true,
      enable_sub_comments: false,
      save_option: 'db',
      cookies: '',
      headless: false,
    }
  }

  function clearMessages() {
    error.value = null
    successMessage.value = null
  }

  function updateFormField<K extends keyof CrawlerStartRequest>(
    field: K,
    value: CrawlerStartRequest[K]
  ) {
    formData.value[field] = value
  }

  return {
    // State
    loading,
    submitting,
    error,
    successMessage,
    crawlerStatus,
    statusLoading,
    serviceAvailable,
    formData,
    
    // Computed
    isRunning,
    isIdle,
    canSubmit,
    
    // Actions
    fetchStatus,
    submitTask,
    startPolling,
    stopPolling,
    resetForm,
    clearMessages,
    updateFormField,
  }
})

