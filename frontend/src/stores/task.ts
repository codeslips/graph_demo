/**
 * Pinia store for crawl task state management.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CrawlTask, CrawlItem, CreateTaskRequest } from '@/types/crawl'
import { createTask, listTasks, getTask, deleteTask, getTaskItems } from '@/api/crawl'

export const useTaskStore = defineStore('task', () => {
  // State
  const tasks = ref<CrawlTask[]>([])
  const currentTask = ref<CrawlTask | null>(null)
  const currentItems = ref<CrawlItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref({
    page: 1,
    pageSize: 20,
    total: 0,
    hasNext: false
  })

  // Getters
  const pendingTasks = computed(() =>
    tasks.value.filter((t) => t.status === 'PENDING')
  )

  const runningTasks = computed(() =>
    tasks.value.filter((t) => t.status === 'RUNNING')
  )

  const completedTasks = computed(() =>
    tasks.value.filter((t) => t.status === 'DONE' || t.status === 'FAILED')
  )

  // Actions
  async function fetchTasks(page: number = 1) {
    loading.value = true
    error.value = null

    try {
      const response = await listTasks({ page, page_size: pagination.value.pageSize })
      tasks.value = response.items
      pagination.value = {
        page: response.page,
        pageSize: response.page_size,
        total: response.total,
        hasNext: response.has_next
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch tasks'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchTask(taskId: string) {
    loading.value = true
    error.value = null

    try {
      currentTask.value = await getTask(taskId)
      return currentTask.value
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch task'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function createNewTask(data: CreateTaskRequest) {
    loading.value = true
    error.value = null

    try {
      const task = await createTask(data)
      tasks.value.unshift(task)
      return task
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create task'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function removeTask(taskId: string) {
    loading.value = true
    error.value = null

    try {
      await deleteTask(taskId)
      tasks.value = tasks.value.filter((t) => t.id !== taskId)
      if (currentTask.value?.id === taskId) {
        currentTask.value = null
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to delete task'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchTaskItems(taskId: string, page: number = 1) {
    loading.value = true
    error.value = null

    try {
      const response = await getTaskItems(taskId, { page, page_size: 50 })
      currentItems.value = response.items
      return response
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch items'
      throw e
    } finally {
      loading.value = false
    }
  }

  function clearCurrentTask() {
    currentTask.value = null
    currentItems.value = []
  }

  return {
    // State
    tasks,
    currentTask,
    currentItems,
    loading,
    error,
    pagination,

    // Getters
    pendingTasks,
    runningTasks,
    completedTasks,

    // Actions
    fetchTasks,
    fetchTask,
    createNewTask,
    removeTask,
    fetchTaskItems,
    clearCurrentTask
  }
})

