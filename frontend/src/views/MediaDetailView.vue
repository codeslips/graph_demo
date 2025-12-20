<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMediaStore, PLATFORM_CONFIGS } from '@/stores/media'
import { getRecord } from '@/api/media'
import type { Platform, MediaRecord } from '@/types/media'

const route = useRoute()
const router = useRouter()
const mediaStore = useMediaStore()

const loading = ref(true)
const error = ref<string | null>(null)
const record = ref<MediaRecord | null>(null)

const platform = computed(() => route.params.platform as Platform)
const entityType = computed(() => route.params.entityType as string)
const recordId = computed(() => Number(route.params.id))

const platformConfig = computed(() =>
  PLATFORM_CONFIGS.find(p => p.id === platform.value)
)

const entityConfig = computed(() =>
  platformConfig.value?.entities.find(e => e.id === entityType.value)
)

const displayFields = computed(() => {
  if (!record.value) return []
  
  return Object.entries(record.value)
    .filter(([key]) => key !== 'id')
    .map(([key, value]) => {
      const column = entityConfig.value?.columns.find(c => c.key === key)
      return {
        key,
        label: column?.label || key,
        value: formatValue(value, column?.type),
        type: column?.type,
      }
    })
})

function formatValue(value: any, type?: string): string {
  if (value === null || value === undefined) return '-'
  
  if (type === 'date' && typeof value === 'number') {
    return new Date(value * 1000).toLocaleString('zh-CN')
  }
  
  if (typeof value === 'object') {
    return JSON.stringify(value)
  }
  
  return String(value)
}

async function fetchRecord() {
  loading.value = true
  error.value = null
  
  try {
    record.value = await getRecord<MediaRecord>(
      platform.value,
      entityConfig.value?.apiPath || entityType.value,
      recordId.value
    )
  } catch (e: any) {
    error.value = e.response?.data?.detail || e.message || '加载失败'
  } finally {
    loading.value = false
  }
}

function handleBack() {
  router.push({ name: 'media' })
}

function handleEdit() {
  if (record.value) {
    // Set context for editing
    mediaStore.setPlatform(platform.value)
    mediaStore.setEntity(entityType.value)
    mediaStore.openEditModal(record.value)
    router.push({ name: 'media' })
  }
}

function handleDelete() {
  if (record.value) {
    mediaStore.setPlatform(platform.value)
    mediaStore.setEntity(entityType.value)
    mediaStore.openDeleteModal([record.value.id])
  }
}

onMounted(() => {
  fetchRecord()
})
</script>

<template>
  <div class="media-detail-view">
    <header class="view-header">
      <button class="back-btn" @click="handleBack">
        ← 返回列表
      </button>
      
      <div class="header-info">
        <span v-if="platformConfig" class="platform-badge">
          {{ platformConfig.icon }} {{ platformConfig.name }}
        </span>
        <span v-if="entityConfig" class="entity-badge">
          {{ entityConfig.name }}
        </span>
      </div>
      
      <div class="header-actions">
        <button class="btn-edit" :disabled="!record" @click="handleEdit">
          ✏️ 编辑
        </button>
        <button class="btn-delete" :disabled="!record" @click="handleDelete">
          🗑️ 删除
        </button>
      </div>
    </header>
    
    <!-- Loading state -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">❌</div>
      <h3>加载失败</h3>
      <p>{{ error }}</p>
      <button class="retry-btn" @click="fetchRecord">重试</button>
    </div>
    
    <!-- Content -->
    <div v-else-if="record" class="detail-content">
      <div class="detail-card">
        <h2>
          记录详情
          <span class="record-id">#{{ record.id }}</span>
        </h2>
        
        <div class="fields-grid">
          <div
            v-for="field in displayFields"
            :key="field.key"
            class="field-item"
          >
            <label>{{ field.label }}</label>
            <div class="field-value" :class="{ 'long-text': String(field.value).length > 100 }">
              {{ field.value }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Delete modal -->
    <Teleport to="body">
      <div
        v-if="mediaStore.showDeleteModal"
        class="modal-backdrop"
        @click.self="mediaStore.closeDeleteModal"
      >
        <div class="modal-content">
          <div class="modal-icon">⚠️</div>
          <h3>确认删除</h3>
          <p>确定要删除这条记录吗？此操作不可撤销！</p>
          <div class="modal-actions">
            <button class="btn-cancel" @click="mediaStore.closeDeleteModal">
              取消
            </button>
            <button
              class="btn-confirm-delete"
              @click="async () => { await mediaStore.confirmDelete(); router.push({ name: 'media' }); }"
            >
              确认删除
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.media-detail-view {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(180deg, #0a0a12 0%, #12121a 100%);
}

.view-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.back-btn {
  padding: 0.5rem 1rem;
  background: rgba(45, 45, 68, 0.8);
  border: 1px solid var(--color-border, #3d3d5c);
  border-radius: 8px;
  color: var(--color-text-secondary, #a0a0b0);
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.back-btn:hover {
  background: rgba(61, 61, 92, 0.8);
  color: var(--color-text-primary, #e0e0e0);
}

.header-info {
  display: flex;
  gap: 0.5rem;
  flex: 1;
}

.platform-badge,
.entity-badge {
  padding: 0.375rem 0.75rem;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 6px;
  font-size: 0.8125rem;
  color: var(--color-accent, #6366f1);
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit,
.btn-delete {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-edit {
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  color: var(--color-accent, #6366f1);
}

.btn-edit:hover:not(:disabled) {
  background: rgba(99, 102, 241, 0.2);
}

.btn-delete {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
}

.btn-delete:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.2);
}

.btn-edit:disabled,
.btn-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.spinner {
  width: 2.5rem;
  height: 2.5rem;
  border: 3px solid var(--color-border, #3d3d5c);
  border-top-color: var(--color-accent, #6366f1);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p,
.error-state p {
  color: var(--color-text-secondary, #a0a0b0);
  margin: 0.5rem 0;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-state h3 {
  margin: 0;
  color: var(--color-text-primary, #e0e0e0);
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: var(--color-accent, #6366f1);
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  transition: opacity 0.2s;
}

.retry-btn:hover {
  opacity: 0.9;
}

.detail-card {
  background: rgba(30, 30, 46, 0.4);
  border: 1px solid var(--color-border, #3d3d5c);
  border-radius: 16px;
  padding: 1.5rem 2rem;
}

.detail-card h2 {
  margin: 0 0 1.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary, #e0e0e0);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.record-id {
  font-size: 0.875rem;
  font-weight: 400;
  color: var(--color-text-secondary, #a0a0b0);
}

.fields-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}

.field-item {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.field-item label {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-text-secondary, #a0a0b0);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.field-value {
  padding: 0.75rem;
  background: rgba(10, 10, 18, 0.4);
  border: 1px solid rgba(61, 61, 92, 0.5);
  border-radius: 8px;
  color: var(--color-text-primary, #e0e0e0);
  font-size: 0.875rem;
  word-break: break-word;
}

.field-value.long-text {
  max-height: 150px;
  overflow-y: auto;
  white-space: pre-wrap;
}

/* Modal styles */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
  border: 1px solid var(--color-border, #3d3d5c);
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  max-width: 400px;
}

.modal-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.modal-content h3 {
  margin: 0 0 0.5rem;
  color: var(--color-text-primary, #e0e0e0);
}

.modal-content p {
  margin: 0 0 1.5rem;
  color: var(--color-text-secondary, #a0a0b0);
  font-size: 0.9375rem;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.btn-cancel,
.btn-confirm-delete {
  padding: 0.625rem 1.5rem;
  border-radius: 8px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: transparent;
  border: 1px solid var(--color-border, #3d3d5c);
  color: var(--color-text-secondary, #a0a0b0);
}

.btn-confirm-delete {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border: none;
  color: white;
}

@media (max-width: 768px) {
  .media-detail-view {
    padding: 1rem;
  }
  
  .fields-grid {
    grid-template-columns: 1fr;
  }
}
</style>

