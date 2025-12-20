/**
 * Media Crawl Pinia Store
 * Manages state for media data management
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  listRecords,
  getRecord,
  createRecord,
  updateRecord,
  deleteRecord,
  batchDeleteRecords,
  getMediaApiStatus,
} from '@/api/media'
import type {
  Platform,
  PlatformConfig,
  EntityConfig,
  FilterParams,
  PaginatedResponse,
  MediaRecord,
  MediaApiStatus,
} from '@/types/media'

// Platform configurations with entity definitions
export const PLATFORM_CONFIGS: PlatformConfig[] = [
  {
    id: 'bilibili',
    name: 'Bilibili',
    icon: '📺',
    entities: [
      {
        id: 'videos',
        name: '视频',
        apiPath: 'videos',
        primaryField: 'video_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'video_id', label: '视频ID', width: 120 },
          { key: 'title', label: '标题', width: 200 },
          { key: 'nickname', label: '用户', width: 120 },
          { key: 'liked_count', label: '点赞', width: 80, type: 'number' },
          { key: 'video_play_count', label: '播放', width: 80 },
          { key: 'create_time', label: '创建时间', width: 150, type: 'date' },
        ],
      },
      {
        id: 'comments',
        name: '评论',
        apiPath: 'comments',
        primaryField: 'comment_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'comment_id', label: '评论ID', width: 120 },
          { key: 'video_id', label: '视频ID', width: 120 },
          { key: 'nickname', label: '用户', width: 120 },
          { key: 'content', label: '内容', width: 200 },
          { key: 'like_count', label: '点赞', width: 80 },
          { key: 'create_time', label: '创建时间', width: 150, type: 'date' },
        ],
      },
      {
        id: 'ups',
        name: 'UP主',
        apiPath: 'ups',
        primaryField: 'user_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'user_id', label: '用户ID', width: 120 },
          { key: 'nickname', label: '昵称', width: 120 },
          { key: 'total_fans', label: '粉丝', width: 100, type: 'number' },
          { key: 'total_liked', label: '获赞', width: 100, type: 'number' },
        ],
      },
      {
        id: 'contacts',
        name: '关注关系',
        apiPath: 'contacts',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'up_id', label: 'UP主ID', width: 120 },
          { key: 'up_name', label: 'UP主名', width: 120 },
          { key: 'fan_id', label: '粉丝ID', width: 120 },
          { key: 'fan_name', label: '粉丝名', width: 120 },
        ],
      },
      {
        id: 'dynamics',
        name: '动态',
        apiPath: 'dynamics',
        primaryField: 'dynamic_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'dynamic_id', label: '动态ID', width: 120 },
          { key: 'user_name', label: '用户', width: 120 },
          { key: 'text', label: '内容', width: 200 },
          { key: 'total_liked', label: '点赞', width: 80, type: 'number' },
          { key: 'pub_ts', label: '发布时间', width: 150, type: 'date' },
        ],
      },
    ],
  },
  {
    id: 'douyin',
    name: '抖音',
    icon: '🎵',
    entities: [
      {
        id: 'awemes',
        name: '作品',
        apiPath: 'awemes',
        primaryField: 'aweme_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'aweme_id', label: '作品ID', width: 120 },
          { key: 'title', label: '标题', width: 200 },
          { key: 'nickname', label: '用户', width: 120 },
          { key: 'liked_count', label: '点赞', width: 80 },
          { key: 'comment_count', label: '评论', width: 80 },
          { key: 'create_time', label: '创建时间', width: 150, type: 'date' },
        ],
      },
      {
        id: 'comments',
        name: '评论',
        apiPath: 'comments',
        primaryField: 'comment_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'comment_id', label: '评论ID', width: 120 },
          { key: 'aweme_id', label: '作品ID', width: 120 },
          { key: 'nickname', label: '用户', width: 120 },
          { key: 'content', label: '内容', width: 200 },
          { key: 'like_count', label: '点赞', width: 80 },
          { key: 'create_time', label: '创建时间', width: 150, type: 'date' },
        ],
      },
      {
        id: 'creators',
        name: '创作者',
        apiPath: 'creators',
        primaryField: 'user_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'user_id', label: '用户ID', width: 120 },
          { key: 'nickname', label: '昵称', width: 120 },
          { key: 'fans', label: '粉丝', width: 100 },
          { key: 'follows', label: '关注', width: 100 },
          { key: 'videos_count', label: '作品数', width: 80 },
        ],
      },
    ],
  },
  {
    id: 'kuaishou',
    name: '快手',
    icon: '🎬',
    entities: [
      {
        id: 'videos',
        name: '视频',
        apiPath: 'videos',
        primaryField: 'video_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'video_id', label: '视频ID', width: 120 },
          { key: 'title', label: '标题', width: 200 },
          { key: 'nickname', label: '用户', width: 120 },
          { key: 'liked_count', label: '点赞', width: 80 },
          { key: 'viewd_count', label: '观看', width: 80 },
          { key: 'create_time', label: '创建时间', width: 150, type: 'date' },
        ],
      },
      {
        id: 'comments',
        name: '评论',
        apiPath: 'comments',
        primaryField: 'comment_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'comment_id', label: '评论ID', width: 120 },
          { key: 'video_id', label: '视频ID', width: 120 },
          { key: 'nickname', label: '用户', width: 120 },
          { key: 'content', label: '内容', width: 200 },
          { key: 'create_time', label: '创建时间', width: 150, type: 'date' },
        ],
      },
    ],
  },
  {
    id: 'weibo',
    name: '微博',
    icon: '📱',
    entities: [
      {
        id: 'notes',
        name: '帖子',
        apiPath: 'notes',
        primaryField: 'note_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'note_id', label: '帖子ID', width: 120 },
          { key: 'nickname', label: '用户', width: 120 },
          { key: 'content', label: '内容', width: 200 },
          { key: 'liked_count', label: '点赞', width: 80 },
          { key: 'comments_count', label: '评论', width: 80 },
          { key: 'create_time', label: '创建时间', width: 150, type: 'date' },
        ],
      },
      {
        id: 'comments',
        name: '评论',
        apiPath: 'comments',
        primaryField: 'comment_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'comment_id', label: '评论ID', width: 120 },
          { key: 'note_id', label: '帖子ID', width: 120 },
          { key: 'nickname', label: '用户', width: 120 },
          { key: 'content', label: '内容', width: 200 },
          { key: 'comment_like_count', label: '点赞', width: 80 },
          { key: 'create_time', label: '创建时间', width: 150, type: 'date' },
        ],
      },
      {
        id: 'creators',
        name: '创作者',
        apiPath: 'creators',
        primaryField: 'user_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'user_id', label: '用户ID', width: 120 },
          { key: 'nickname', label: '昵称', width: 120 },
          { key: 'fans', label: '粉丝', width: 100 },
          { key: 'follows', label: '关注', width: 100 },
        ],
      },
    ],
  },
  {
    id: 'xhs',
    name: '小红书',
    icon: '📕',
    entities: [
      {
        id: 'notes',
        name: '笔记',
        apiPath: 'notes',
        primaryField: 'note_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'note_id', label: '笔记ID', width: 120 },
          { key: 'title', label: '标题', width: 200 },
          { key: 'nickname', label: '用户', width: 120 },
          { key: 'liked_count', label: '点赞', width: 80 },
          { key: 'collected_count', label: '收藏', width: 80 },
          { key: 'time', label: '发布时间', width: 150, type: 'date' },
        ],
      },
      {
        id: 'comments',
        name: '评论',
        apiPath: 'comments',
        primaryField: 'comment_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'comment_id', label: '评论ID', width: 120 },
          { key: 'note_id', label: '笔记ID', width: 120 },
          { key: 'nickname', label: '用户', width: 120 },
          { key: 'content', label: '内容', width: 200 },
          { key: 'like_count', label: '点赞', width: 80 },
          { key: 'create_time', label: '创建时间', width: 150, type: 'date' },
        ],
      },
      {
        id: 'creators',
        name: '创作者',
        apiPath: 'creators',
        primaryField: 'user_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'user_id', label: '用户ID', width: 120 },
          { key: 'nickname', label: '昵称', width: 120 },
          { key: 'fans', label: '粉丝', width: 100 },
          { key: 'follows', label: '关注', width: 100 },
        ],
      },
    ],
  },
  {
    id: 'tieba',
    name: '贴吧',
    icon: '💬',
    entities: [
      {
        id: 'notes',
        name: '帖子',
        apiPath: 'notes',
        primaryField: 'note_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'note_id', label: '帖子ID', width: 120 },
          { key: 'title', label: '标题', width: 200 },
          { key: 'user_nickname', label: '用户', width: 120 },
          { key: 'tieba_name', label: '贴吧', width: 120 },
          { key: 'total_replay_num', label: '回复', width: 80, type: 'number' },
          { key: 'publish_time', label: '发布时间', width: 150 },
        ],
      },
      {
        id: 'comments',
        name: '评论',
        apiPath: 'comments',
        primaryField: 'comment_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'comment_id', label: '评论ID', width: 120 },
          { key: 'note_id', label: '帖子ID', width: 120 },
          { key: 'user_nickname', label: '用户', width: 120 },
          { key: 'content', label: '内容', width: 200 },
          { key: 'publish_time', label: '发布时间', width: 150 },
        ],
      },
      {
        id: 'creators',
        name: '创作者',
        apiPath: 'creators',
        primaryField: 'user_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'user_id', label: '用户ID', width: 120 },
          { key: 'nickname', label: '昵称', width: 120 },
          { key: 'fans', label: '粉丝', width: 100 },
          { key: 'follows', label: '关注', width: 100 },
        ],
      },
    ],
  },
  {
    id: 'zhihu',
    name: '知乎',
    icon: '📖',
    entities: [
      {
        id: 'contents',
        name: '内容',
        apiPath: 'contents',
        primaryField: 'content_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'content_id', label: '内容ID', width: 120 },
          { key: 'content_type', label: '类型', width: 80 },
          { key: 'title', label: '标题', width: 200 },
          { key: 'user_nickname', label: '用户', width: 120 },
          { key: 'voteup_count', label: '赞同', width: 80, type: 'number' },
          { key: 'comment_count', label: '评论', width: 80, type: 'number' },
          { key: 'created_time', label: '创建时间', width: 150 },
        ],
      },
      {
        id: 'comments',
        name: '评论',
        apiPath: 'comments',
        primaryField: 'comment_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'comment_id', label: '评论ID', width: 120 },
          { key: 'content_id', label: '内容ID', width: 120 },
          { key: 'user_nickname', label: '用户', width: 120 },
          { key: 'content', label: '内容', width: 200 },
          { key: 'like_count', label: '点赞', width: 80, type: 'number' },
          { key: 'publish_time', label: '发布时间', width: 150 },
        ],
      },
      {
        id: 'creators',
        name: '创作者',
        apiPath: 'creators',
        primaryField: 'user_id',
        columns: [
          { key: 'id', label: 'ID', width: 80 },
          { key: 'user_id', label: '用户ID', width: 120 },
          { key: 'user_nickname', label: '昵称', width: 120 },
          { key: 'fans', label: '粉丝', width: 100, type: 'number' },
          { key: 'follows', label: '关注', width: 100, type: 'number' },
          { key: 'anwser_count', label: '回答', width: 80, type: 'number' },
        ],
      },
    ],
  },
]

export const useMediaStore = defineStore('media', () => {
  // State
  const loading = ref(false)
  const error = ref<string | null>(null)
  const apiStatus = ref<MediaApiStatus | null>(null)
  
  const currentPlatform = ref<Platform>('bilibili')
  const currentEntityId = ref<string>('videos')
  
  const records = ref<MediaRecord[]>([])
  const selectedIds = ref<number[]>([])
  
  const pagination = ref({
    total: 0,
    limit: 20,
    offset: 0,
  })
  
  const filters = ref<FilterParams>({})
  
  // Modal state
  const showFormModal = ref(false)
  const showDeleteModal = ref(false)
  const editingRecord = ref<MediaRecord | null>(null)
  const deletingIds = ref<number[]>([])

  // Computed
  const currentPlatformConfig = computed(() =>
    PLATFORM_CONFIGS.find(p => p.id === currentPlatform.value)
  )
  
  const currentEntityConfig = computed(() =>
    currentPlatformConfig.value?.entities.find(e => e.id === currentEntityId.value)
  )
  
  const currentPage = computed(() =>
    Math.floor(pagination.value.offset / pagination.value.limit) + 1
  )
  
  const totalPages = computed(() =>
    Math.ceil(pagination.value.total / pagination.value.limit)
  )
  
  const isEnabled = computed(() => apiStatus.value?.enabled ?? true)

  // Actions
  async function fetchApiStatus() {
    try {
      apiStatus.value = await getMediaApiStatus()
    } catch (e) {
      console.error('Failed to fetch API status:', e)
    }
  }

  async function fetchRecords() {
    if (!currentPlatformConfig.value || !currentEntityConfig.value) return
    
    loading.value = true
    error.value = null
    
    try {
      const response = await listRecords<MediaRecord>(
        currentPlatform.value,
        currentEntityConfig.value.apiPath,
        {
          ...filters.value,
          limit: pagination.value.limit,
          offset: pagination.value.offset,
        }
      )
      
      records.value = response.items
      pagination.value.total = response.total
    } catch (e: any) {
      error.value = e.response?.data?.detail || e.message || '加载数据失败'
      records.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchSingleRecord(id: number): Promise<MediaRecord | null> {
    if (!currentPlatformConfig.value || !currentEntityConfig.value) return null
    
    try {
      return await getRecord<MediaRecord>(
        currentPlatform.value,
        currentEntityConfig.value.apiPath,
        id
      )
    } catch (e: any) {
      error.value = e.response?.data?.detail || e.message || '加载记录失败'
      return null
    }
  }

  async function saveRecord(data: Partial<MediaRecord>): Promise<boolean> {
    if (!currentPlatformConfig.value || !currentEntityConfig.value) return false
    
    loading.value = true
    error.value = null
    
    try {
      if (editingRecord.value) {
        await updateRecord(
          currentPlatform.value,
          currentEntityConfig.value.apiPath,
          editingRecord.value.id,
          data
        )
      } else {
        await createRecord(
          currentPlatform.value,
          currentEntityConfig.value.apiPath,
          data
        )
      }
      
      await fetchRecords()
      closeFormModal()
      return true
    } catch (e: any) {
      error.value = e.response?.data?.detail || e.message || '保存失败'
      return false
    } finally {
      loading.value = false
    }
  }

  async function confirmDelete(): Promise<boolean> {
    if (!currentPlatformConfig.value || !currentEntityConfig.value) return false
    if (deletingIds.value.length === 0) return false
    
    loading.value = true
    error.value = null
    
    try {
      if (deletingIds.value.length === 1) {
        await deleteRecord(
          currentPlatform.value,
          currentEntityConfig.value.apiPath,
          deletingIds.value[0]
        )
      } else {
        await batchDeleteRecords(
          currentPlatform.value,
          currentEntityConfig.value.apiPath,
          deletingIds.value
        )
      }
      
      selectedIds.value = selectedIds.value.filter(id => !deletingIds.value.includes(id))
      await fetchRecords()
      closeDeleteModal()
      return true
    } catch (e: any) {
      error.value = e.response?.data?.detail || e.message || '删除失败'
      return false
    } finally {
      loading.value = false
    }
  }

  function setPlatform(platform: Platform) {
    currentPlatform.value = platform
    const config = PLATFORM_CONFIGS.find(p => p.id === platform)
    if (config && config.entities.length > 0) {
      currentEntityId.value = config.entities[0].id
    }
    resetPagination()
    clearSelection()
  }

  function setEntity(entityId: string) {
    currentEntityId.value = entityId
    resetPagination()
    clearSelection()
  }

  function setPage(page: number) {
    pagination.value.offset = (page - 1) * pagination.value.limit
  }

  function setFilters(newFilters: FilterParams) {
    filters.value = newFilters
    resetPagination()
  }

  function clearFilters() {
    filters.value = {}
    resetPagination()
  }

  function resetPagination() {
    pagination.value.offset = 0
    pagination.value.total = 0
  }

  function toggleSelection(id: number) {
    const index = selectedIds.value.indexOf(id)
    if (index === -1) {
      selectedIds.value.push(id)
    } else {
      selectedIds.value.splice(index, 1)
    }
  }

  function selectAll() {
    selectedIds.value = records.value.map(r => r.id)
  }

  function clearSelection() {
    selectedIds.value = []
  }

  function openCreateModal() {
    editingRecord.value = null
    showFormModal.value = true
  }

  function openEditModal(record: MediaRecord) {
    editingRecord.value = record
    showFormModal.value = true
  }

  function closeFormModal() {
    showFormModal.value = false
    editingRecord.value = null
  }

  function openDeleteModal(ids: number[]) {
    deletingIds.value = ids
    showDeleteModal.value = true
  }

  function closeDeleteModal() {
    showDeleteModal.value = false
    deletingIds.value = []
  }

  return {
    // State
    loading,
    error,
    apiStatus,
    currentPlatform,
    currentEntityId,
    records,
    selectedIds,
    pagination,
    filters,
    showFormModal,
    showDeleteModal,
    editingRecord,
    deletingIds,
    
    // Computed
    currentPlatformConfig,
    currentEntityConfig,
    currentPage,
    totalPages,
    isEnabled,
    
    // Actions
    fetchApiStatus,
    fetchRecords,
    fetchSingleRecord,
    saveRecord,
    confirmDelete,
    setPlatform,
    setEntity,
    setPage,
    setFilters,
    clearFilters,
    toggleSelection,
    selectAll,
    clearSelection,
    openCreateModal,
    openEditModal,
    closeFormModal,
    openDeleteModal,
    closeDeleteModal,
  }
})

