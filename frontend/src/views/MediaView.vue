<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useMediaStore } from '@/stores/media'
import PlatformTabs from '@/components/media/PlatformTabs.vue'
import MediaFilters from '@/components/media/MediaFilters.vue'
import MediaDataTable from '@/components/media/MediaDataTable.vue'
import MediaFormModal from '@/components/media/MediaFormModal.vue'
import DeleteConfirmModal from '@/components/media/DeleteConfirmModal.vue'

const mediaStore = useMediaStore()

onMounted(async () => {
  await mediaStore.fetchApiStatus()
  await mediaStore.fetchRecords()
})

// Refetch when platform or entity changes
watch(
  [() => mediaStore.currentPlatform, () => mediaStore.currentEntityId],
  async () => {
    await mediaStore.fetchRecords()
  }
)

function handleCreate() {
  mediaStore.openCreateModal()
}

function handleBatchDelete() {
  if (mediaStore.selectedIds.length > 0) {
    mediaStore.openDeleteModal(mediaStore.selectedIds)
  }
}
</script>

<template>
  <div class="media-view">
    <header class="view-header">
      <div class="header-content">
        <h1>媒体数据管理</h1>
        <p class="subtitle">管理各平台爬取数据</p>
      </div>
      
      <div class="header-actions">
        <button
          v-if="mediaStore.selectedIds.length > 0"
          class="btn-batch-delete"
          @click="handleBatchDelete"
        >
          🗑️ 批量删除 ({{ mediaStore.selectedIds.length }})
        </button>
        <button class="btn-create" @click="handleCreate">
          ➕ 新建
        </button>
      </div>
    </header>
    
    <!-- Disabled warning -->
    <div v-if="!mediaStore.isEnabled" class="disabled-warning">
      <span class="warning-icon">⚠️</span>
      <span>媒体数据功能当前已禁用</span>
    </div>
    
    <!-- Error display -->
    <div v-if="mediaStore.error" class="error-banner">
      <span class="error-icon">❌</span>
      <span>{{ mediaStore.error }}</span>
      <button class="dismiss-btn" @click="mediaStore.error = null">✕</button>
    </div>
    
    <div class="view-content">
      <!-- Platform tabs -->
      <PlatformTabs />
      
      <!-- Filters -->
      <MediaFilters />
      
      <!-- Data table -->
      <MediaDataTable />
    </div>
    
    <!-- Modals -->
    <MediaFormModal />
    <DeleteConfirmModal />
  </div>
</template>

<style scoped>
.media-view {
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(180deg, #0a0a12 0%, #12121a 100%);
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-content h1 {
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

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.btn-create,
.btn-batch-delete {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-create {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  color: white;
}

.btn-create:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-batch-delete {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
}

.btn-batch-delete:hover {
  background: rgba(239, 68, 68, 0.2);
}

.disabled-warning,
.error-banner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.disabled-warning {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
  color: #fbbf24;
}

.error-banner {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
}

.warning-icon,
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
  transition: opacity 0.2s;
}

.dismiss-btn:hover {
  opacity: 1;
}

.view-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .media-view {
    padding: 1rem;
  }
  
  .view-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: flex-end;
  }
}
</style>

