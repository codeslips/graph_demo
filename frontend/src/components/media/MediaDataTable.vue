<script setup lang="ts">
import { computed } from 'vue'
import { useMediaStore } from '@/stores/media'
import { useRouter } from 'vue-router'
import type { MediaRecord } from '@/types/media'

const router = useRouter()
const mediaStore = useMediaStore()

const columns = computed(() => mediaStore.currentEntityConfig?.columns || [])

const allSelected = computed(() => {
  if (mediaStore.records.length === 0) return false
  return mediaStore.selectedIds.length === mediaStore.records.length
})

const someSelected = computed(() => {
  return mediaStore.selectedIds.length > 0 && !allSelected.value
})

function formatCellValue(record: MediaRecord, key: string, type?: string): string {
  const value = (record as any)[key]
  if (value === null || value === undefined) return '-'
  
  if (type === 'date' && typeof value === 'number') {
    // Assuming timestamp in seconds
    const date = new Date(value * 1000)
    return date.toLocaleString('zh-CN')
  }
  
  if (typeof value === 'string' && value.length > 50) {
    return value.substring(0, 50) + '...'
  }
  
  return String(value)
}

function isSelected(id: number): boolean {
  return mediaStore.selectedIds.includes(id)
}

function toggleSelectAll() {
  if (allSelected.value) {
    mediaStore.clearSelection()
  } else {
    mediaStore.selectAll()
  }
}

function handleRowClick(record: MediaRecord) {
  router.push({
    name: 'media-detail',
    params: {
      platform: mediaStore.currentPlatform,
      entityType: mediaStore.currentEntityId,
      id: record.id,
    },
  })
}

function handleEdit(e: Event, record: MediaRecord) {
  e.stopPropagation()
  mediaStore.openEditModal(record)
}

function handleDelete(e: Event, record: MediaRecord) {
  e.stopPropagation()
  mediaStore.openDeleteModal([record.id])
}

function handlePageChange(page: number) {
  mediaStore.setPage(page)
  mediaStore.fetchRecords()
}
</script>

<template>
  <div class="media-data-table">
    <!-- Table -->
    <div class="table-container">
      <table v-if="!mediaStore.loading && mediaStore.records.length > 0">
        <thead>
          <tr>
            <th class="checkbox-col">
              <input
                type="checkbox"
                :checked="allSelected"
                :indeterminate="someSelected"
                @change="toggleSelectAll"
              />
            </th>
            <th
              v-for="col in columns"
              :key="col.key"
              :style="{ width: col.width ? `${col.width}px` : 'auto' }"
            >
              {{ col.label }}
            </th>
            <th class="actions-col">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="record in mediaStore.records"
            :key="record.id"
            :class="{ selected: isSelected(record.id) }"
            @click="handleRowClick(record)"
          >
            <td class="checkbox-col" @click.stop>
              <input
                type="checkbox"
                :checked="isSelected(record.id)"
                @change="mediaStore.toggleSelection(record.id)"
              />
            </td>
            <td
              v-for="col in columns"
              :key="col.key"
              :title="String((record as any)[col.key] || '')"
            >
              {{ formatCellValue(record, col.key, col.type) }}
            </td>
            <td class="actions-col">
              <button class="action-btn edit" title="编辑" @click="handleEdit($event, record)">
                ✏️
              </button>
              <button class="action-btn delete" title="删除" @click="handleDelete($event, record)">
                🗑️
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <!-- Loading state -->
      <div v-if="mediaStore.loading" class="table-loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
      
      <!-- Empty state -->
      <div v-else-if="mediaStore.records.length === 0" class="table-empty">
        <div class="empty-icon">📭</div>
        <p>暂无数据</p>
      </div>
    </div>
    
    <!-- Pagination -->
    <div v-if="mediaStore.pagination.total > 0" class="pagination">
      <div class="pagination-info">
        共 {{ mediaStore.pagination.total }} 条记录
      </div>
      <div class="pagination-controls">
        <button
          class="page-btn"
          :disabled="mediaStore.currentPage === 1"
          @click="handlePageChange(mediaStore.currentPage - 1)"
        >
          上一页
        </button>
        
        <span class="page-indicator">
          {{ mediaStore.currentPage }} / {{ mediaStore.totalPages }}
        </span>
        
        <button
          class="page-btn"
          :disabled="mediaStore.currentPage === mediaStore.totalPages"
          @click="handlePageChange(mediaStore.currentPage + 1)"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.media-data-table {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.table-container {
  overflow-x: auto;
  background: rgba(30, 30, 46, 0.4);
  border: 1px solid var(--color-border, #3d3d5c);
  border-radius: 12px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

thead {
  background: rgba(99, 102, 241, 0.1);
}

th {
  padding: 0.875rem 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--color-text-secondary, #a0a0b0);
  border-bottom: 1px solid var(--color-border, #3d3d5c);
  white-space: nowrap;
}

tbody tr {
  cursor: pointer;
  transition: background 0.15s ease;
}

tbody tr:hover {
  background: rgba(99, 102, 241, 0.05);
}

tbody tr.selected {
  background: rgba(99, 102, 241, 0.1);
}

td {
  padding: 0.75rem 1rem;
  color: var(--color-text-primary, #e0e0e0);
  border-bottom: 1px solid rgba(61, 61, 92, 0.5);
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.checkbox-col {
  width: 40px;
  text-align: center;
}

.checkbox-col input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: var(--color-accent, #6366f1);
}

.actions-col {
  width: 100px;
  text-align: center;
}

.action-btn {
  padding: 0.375rem;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.action-btn:hover {
  opacity: 1;
}

.table-loading,
.table-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: var(--color-text-secondary, #a0a0b0);
}

.spinner {
  width: 2rem;
  height: 2rem;
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

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.pagination-info {
  font-size: 0.875rem;
  color: var(--color-text-secondary, #a0a0b0);
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  background: rgba(45, 45, 68, 0.8);
  border: 1px solid var(--color-border, #3d3d5c);
  border-radius: 6px;
  color: var(--color-text-primary, #e0e0e0);
  cursor: pointer;
  font-size: 0.8125rem;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: rgba(61, 61, 92, 0.8);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-indicator {
  font-size: 0.875rem;
  color: var(--color-text-secondary, #a0a0b0);
  min-width: 80px;
  text-align: center;
}
</style>

