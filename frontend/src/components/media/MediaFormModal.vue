<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useMediaStore } from '@/stores/media'
import type { MediaRecord } from '@/types/media'

const mediaStore = useMediaStore()

const formData = ref<Record<string, any>>({})
const submitting = ref(false)

const isEditing = computed(() => !!mediaStore.editingRecord)
const modalTitle = computed(() => isEditing.value ? '编辑记录' : '新建记录')

// Get form fields from current entity config columns
const formFields = computed(() => {
  if (!mediaStore.currentEntityConfig) return []
  
  // Exclude 'id' field for the form
  return mediaStore.currentEntityConfig.columns
    .filter(col => col.key !== 'id')
    .map(col => ({
      key: col.key,
      label: col.label,
      type: col.type === 'number' ? 'number' : col.type === 'date' ? 'datetime-local' : 'text',
    }))
})

// Initialize form data when modal opens
watch(() => mediaStore.showFormModal, (show) => {
  if (show) {
    if (mediaStore.editingRecord) {
      // Copy all record fields for editing
      formData.value = { ...mediaStore.editingRecord }
    } else {
      // Reset form for new record
      formData.value = {}
    }
  }
}, { immediate: true })

async function handleSubmit() {
  submitting.value = true
  
  // Convert date fields back to timestamps
  const data = { ...formData.value }
  formFields.value.forEach(field => {
    if (field.type === 'datetime-local' && data[field.key]) {
      data[field.key] = Math.floor(new Date(data[field.key]).getTime() / 1000)
    }
  })
  
  await mediaStore.saveRecord(data)
  submitting.value = false
}

function handleClose() {
  mediaStore.closeFormModal()
}

function handleBackdropClick(e: MouseEvent) {
  if ((e.target as HTMLElement).classList.contains('modal-backdrop')) {
    handleClose()
  }
}

function formatDateForInput(timestamp: number | undefined): string {
  if (!timestamp) return ''
  const date = new Date(timestamp * 1000)
  return date.toISOString().slice(0, 16)
}

function getFieldValue(key: string, type: string): any {
  const value = formData.value[key]
  if (type === 'datetime-local' && typeof value === 'number') {
    return formatDateForInput(value)
  }
  return value ?? ''
}

function setFieldValue(key: string, type: string, value: any) {
  if (type === 'number' && value !== '') {
    formData.value[key] = Number(value)
  } else {
    formData.value[key] = value
  }
}
</script>

<template>
  <Teleport to="body">
    <div
      v-if="mediaStore.showFormModal"
      class="modal-backdrop"
      @click="handleBackdropClick"
    >
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button class="close-btn" @click="handleClose">✕</button>
        </div>
        
        <form class="modal-body" @submit.prevent="handleSubmit">
          <div class="form-grid">
            <div
              v-for="field in formFields"
              :key="field.key"
              class="form-group"
            >
              <label :for="`field-${field.key}`">{{ field.label }}</label>
              <input
                :id="`field-${field.key}`"
                :type="field.type"
                :value="getFieldValue(field.key, field.type)"
                @input="setFieldValue(field.key, field.type, ($event.target as HTMLInputElement).value)"
              />
            </div>
          </div>
          
          <div v-if="mediaStore.error" class="form-error">
            {{ mediaStore.error }}
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="handleClose">
              取消
            </button>
            <button
              type="submit"
              class="btn-submit"
              :disabled="submitting"
            >
              {{ submitting ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
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
  width: 100%;
  max-width: 600px;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--color-border, #3d3d5c);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-primary, #e0e0e0);
}

.close-btn {
  padding: 0.5rem;
  background: transparent;
  border: none;
  color: var(--color-text-secondary, #a0a0b0);
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  transition: color 0.2s;
}

.close-btn:hover {
  color: var(--color-text-primary, #e0e0e0);
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.form-group label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--color-text-secondary, #a0a0b0);
}

.form-group input {
  padding: 0.625rem 0.75rem;
  background: rgba(10, 10, 18, 0.6);
  border: 1px solid var(--color-border, #3d3d5c);
  border-radius: 6px;
  color: var(--color-text-primary, #e0e0e0);
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--color-accent, #6366f1);
}

.form-error {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #f87171;
  font-size: 0.875rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border, #3d3d5c);
}

.btn-cancel,
.btn-submit {
  padding: 0.625rem 1.25rem;
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

.btn-submit {
  background: linear-gradient(135deg, var(--color-accent, #6366f1) 0%, #8b5cf6 100%);
  border: none;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-backdrop {
    padding: 1rem;
  }
}
</style>

