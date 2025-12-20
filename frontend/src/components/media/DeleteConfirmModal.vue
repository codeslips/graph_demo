<script setup lang="ts">
import { computed, ref } from 'vue'
import { useMediaStore } from '@/stores/media'

const mediaStore = useMediaStore()
const deleting = ref(false)

const deleteCount = computed(() => mediaStore.deletingIds.length)
const isBatch = computed(() => deleteCount.value > 1)

async function handleConfirm() {
  deleting.value = true
  await mediaStore.confirmDelete()
  deleting.value = false
}

function handleCancel() {
  mediaStore.closeDeleteModal()
}

function handleBackdropClick(e: MouseEvent) {
  if ((e.target as HTMLElement).classList.contains('modal-backdrop')) {
    handleCancel()
  }
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="mediaStore.showDeleteModal"
      class="modal-backdrop"
      @click="handleBackdropClick"
    >
      <div class="modal-content">
        <div class="modal-icon">⚠️</div>
        
        <h3 class="modal-title">确认删除</h3>
        
        <p class="modal-message">
          <template v-if="isBatch">
            确定要删除选中的 <strong>{{ deleteCount }}</strong> 条记录吗？
          </template>
          <template v-else>
            确定要删除这条记录吗？
          </template>
        </p>
        
        <p class="modal-warning">此操作不可撤销！</p>
        
        <div v-if="mediaStore.error" class="modal-error">
          {{ mediaStore.error }}
        </div>
        
        <div class="modal-actions">
          <button class="btn-cancel" @click="handleCancel">
            取消
          </button>
          <button
            class="btn-delete"
            :disabled="deleting"
            @click="handleConfirm"
          >
            {{ deleting ? '删除中...' : '确认删除' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
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
  border: 1px solid var(--color-border, #3d3d5c);
  border-radius: 16px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modal-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.modal-title {
  margin: 0 0 1rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary, #e0e0e0);
}

.modal-message {
  margin: 0 0 0.5rem;
  color: var(--color-text-secondary, #a0a0b0);
  font-size: 0.9375rem;
  line-height: 1.5;
}

.modal-message strong {
  color: var(--color-accent, #6366f1);
}

.modal-warning {
  margin: 0 0 1.5rem;
  color: #f87171;
  font-size: 0.8125rem;
}

.modal-error {
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #f87171;
  font-size: 0.875rem;
  text-align: left;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.btn-cancel,
.btn-delete {
  padding: 0.625rem 1.5rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: transparent;
  border: 1px solid var(--color-border, #3d3d5c);
  color: var(--color-text-secondary, #a0a0b0);
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text-primary, #e0e0e0);
}

.btn-delete {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border: none;
  color: white;
}

.btn-delete:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-delete:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}
</style>

