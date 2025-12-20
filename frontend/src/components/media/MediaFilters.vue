<script setup lang="ts">
import { ref, watch } from 'vue'
import { useMediaStore } from '@/stores/media'
import type { FilterParams } from '@/types/media'

const mediaStore = useMediaStore()

const userId = ref('')
const sourceKeyword = ref('')
const dateFrom = ref('')
const dateTo = ref('')

// Sync local state with store filters
watch(() => mediaStore.filters, (newFilters) => {
  userId.value = newFilters.user_id || ''
  sourceKeyword.value = newFilters.source_keyword || ''
}, { immediate: true })

function handleSearch() {
  const filters: FilterParams = {}
  
  if (userId.value.trim()) {
    filters.user_id = userId.value.trim()
  }
  if (sourceKeyword.value.trim()) {
    filters.source_keyword = sourceKeyword.value.trim()
  }
  if (dateFrom.value) {
    filters.create_time_from = Math.floor(new Date(dateFrom.value).getTime() / 1000)
  }
  if (dateTo.value) {
    filters.create_time_to = Math.floor(new Date(dateTo.value).getTime() / 1000)
  }
  
  mediaStore.setFilters(filters)
  mediaStore.fetchRecords()
}

function handleClear() {
  userId.value = ''
  sourceKeyword.value = ''
  dateFrom.value = ''
  dateTo.value = ''
  mediaStore.clearFilters()
  mediaStore.fetchRecords()
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter') {
    handleSearch()
  }
}
</script>

<template>
  <div class="media-filters">
    <div class="filter-row">
      <div class="filter-group">
        <label>用户ID</label>
        <input
          v-model="userId"
          type="text"
          placeholder="输入用户ID"
          @keydown="handleKeydown"
        />
      </div>
      
      <div class="filter-group">
        <label>关键词</label>
        <input
          v-model="sourceKeyword"
          type="text"
          placeholder="来源关键词"
          @keydown="handleKeydown"
        />
      </div>
      
      <div class="filter-group date-group">
        <label>时间范围</label>
        <div class="date-inputs">
          <input
            v-model="dateFrom"
            type="date"
            placeholder="开始日期"
          />
          <span class="date-separator">至</span>
          <input
            v-model="dateTo"
            type="date"
            placeholder="结束日期"
          />
        </div>
      </div>
      
      <div class="filter-actions">
        <button class="btn-search" @click="handleSearch">
          🔍 搜索
        </button>
        <button class="btn-clear" @click="handleClear">
          清除
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.media-filters {
  background: rgba(30, 30, 46, 0.4);
  border: 1px solid var(--color-border, #3d3d5c);
  border-radius: 12px;
  padding: 1rem 1.25rem;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  min-width: 150px;
}

.filter-group label {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-text-secondary, #a0a0b0);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.filter-group input {
  padding: 0.5rem 0.75rem;
  background: rgba(10, 10, 18, 0.6);
  border: 1px solid var(--color-border, #3d3d5c);
  border-radius: 6px;
  color: var(--color-text-primary, #e0e0e0);
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.filter-group input:focus {
  outline: none;
  border-color: var(--color-accent, #6366f1);
}

.filter-group input::placeholder {
  color: var(--color-text-secondary, #6a6a80);
}

.date-group {
  min-width: 280px;
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-inputs input {
  flex: 1;
  min-width: 0;
}

.date-separator {
  color: var(--color-text-secondary, #a0a0b0);
  font-size: 0.8125rem;
}

.filter-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: auto;
}

.btn-search,
.btn-clear {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-search {
  background: linear-gradient(135deg, var(--color-accent, #6366f1) 0%, #8b5cf6 100%);
  border: none;
  color: white;
}

.btn-search:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-clear {
  background: transparent;
  border: 1px solid var(--color-border, #3d3d5c);
  color: var(--color-text-secondary, #a0a0b0);
}

.btn-clear:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text-primary, #e0e0e0);
}

@media (max-width: 768px) {
  .filter-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .filter-actions {
    margin-left: 0;
    justify-content: flex-end;
  }
}
</style>

