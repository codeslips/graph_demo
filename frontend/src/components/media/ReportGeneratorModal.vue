<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useMediaStore } from '@/stores/media'
import { getSourceKeywords, exportMediaData, createReport } from '@/api/report'
import { sendChatMessage } from '@/api/coze'
import type { ExportDataRequest, ReportCreateRequest } from '@/types/report'

const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'saved'): void
}>()

const mediaStore = useMediaStore()

// Form state
const sourceKeyword = ref('')
const timeFrom = ref('')
const timeTo = ref('')
const availableKeywords = ref<string[]>([])
const keywordError = ref('')
const loadingKeywords = ref(false)
const showKeywordDropdown = ref(false)

// Generation state
const generating = ref(false)
const generatedReport = ref('')
const reportPreviewRef = ref<HTMLDivElement | null>(null)
const exportRecordCount = ref(0)
const exportTruncated = ref(false)

// Save state
const saving = ref(false)
const saveError = ref('')
const saveSuccess = ref(false)

const currentPlatform = computed(() => mediaStore.currentPlatform)

// Load available keywords when platform changes
watch(currentPlatform, async () => {
  await loadKeywords()
}, { immediate: true })

async function loadKeywords() {
  if (!currentPlatform.value) return
  
  loadingKeywords.value = true
  keywordError.value = ''
  try {
    const response = await getSourceKeywords(currentPlatform.value)
    availableKeywords.value = response.keywords
    // Re-validate after keywords loaded if user already typed something
    if (sourceKeyword.value) {
      validateKeyword()
    }
  } catch (e) {
    console.error('Failed to load keywords:', e)
    availableKeywords.value = []
  } finally {
    loadingKeywords.value = false
  }
}

function validateKeyword() {
  if (!sourceKeyword.value) {
    keywordError.value = ''
    return
  }
  if (loadingKeywords.value) {
    // Don't validate while loading
    keywordError.value = ''
    return
  }
  if (availableKeywords.value.length === 0) {
    // Keywords not loaded yet or empty
    keywordError.value = ''
    return
  }
  if (!availableKeywords.value.includes(sourceKeyword.value)) {
    keywordError.value = '该关键词不存在于数据库中，请从列表中选择'
  } else {
    keywordError.value = ''
  }
}

// Filter keywords for autocomplete
const filteredKeywords = computed(() => {
  if (!sourceKeyword.value) {
    return availableKeywords.value.slice(0, 15)
  }
  const lower = sourceKeyword.value.toLowerCase()
  return availableKeywords.value
    .filter(k => k.toLowerCase().includes(lower))
    .slice(0, 15)
})

// Check if current keyword is valid (only when keywords are loaded)
const isKeywordValid = computed(() => {
  if (!sourceKeyword.value) return false
  if (loadingKeywords.value) return false  // Still loading
  if (availableKeywords.value.length === 0) return false  // No keywords available
  return availableKeywords.value.includes(sourceKeyword.value)
})

// Check if we're still checking validity (keywords loading)
const isValidating = computed(() => {
  return sourceKeyword.value && loadingKeywords.value
})

function selectKeyword(keyword: string) {
  sourceKeyword.value = keyword
  keywordError.value = ''
  showKeywordDropdown.value = false
}

function handleKeywordFocus() {
  showKeywordDropdown.value = true
}

function handleKeywordBlur() {
  // Delay to allow click on dropdown options
  setTimeout(() => {
    showKeywordDropdown.value = false
    // Validate on blur only if keywords are loaded
    validateKeyword()
  }, 200)
}

function handleKeywordInput() {
  // Clear error while typing
  keywordError.value = ''
}

function parseTimeToTimestamp(dateStr: string): number | null {
  if (!dateStr) return null
  // For date input (YYYY-MM-DD format), set to start of day
  const date = new Date(dateStr + 'T00:00:00')
  return Math.floor(date.getTime() / 1000)
}

async function handleGenerate() {
  // Validate
  if (!sourceKeyword.value) {
    keywordError.value = '请输入来源关键词'
    return
  }
  if (!availableKeywords.value.includes(sourceKeyword.value)) {
    keywordError.value = '该关键词不存在于数据库中，请从列表中选择'
    return
  }

  generating.value = true
  generatedReport.value = ''
  saveSuccess.value = false
  saveError.value = ''

  try {
    // Step 1: Export data
    const exportRequest: ExportDataRequest = {
      platform: currentPlatform.value,
      source_keyword: sourceKeyword.value,
      time_from: parseTimeToTimestamp(timeFrom.value),
      time_to: parseTimeToTimestamp(timeTo.value),
    }

    const exportResponse = await exportMediaData(exportRequest)
    exportRecordCount.value = exportResponse.record_count
    exportTruncated.value = exportResponse.truncated

    if (exportResponse.record_count === 0) {
      generatedReport.value = '没有找到符合条件的数据。'
      generating.value = false
      return
    }

    // Step 2: Send to Coze for analysis
    const message = exportResponse.csv_data

    await sendChatMessage(
      { message },
      {
        onMessage: (content: string) => {
          generatedReport.value += content
          scrollToBottom()
        },
        onError: (err: string) => {
          generatedReport.value += `\n\n**错误**: ${err}`
          generating.value = false
        },
        onComplete: () => {
          generating.value = false
        }
      }
    )
  } catch (e: any) {
    console.error('Failed to generate report:', e)
    generatedReport.value = `生成报告时出错: ${e.message || '未知错误'}`
    generating.value = false
  }
}

function scrollToBottom() {
  if (reportPreviewRef.value) {
    reportPreviewRef.value.scrollTop = reportPreviewRef.value.scrollHeight
  }
}

async function handleSave() {
  if (!generatedReport.value || generating.value) return

  saving.value = true
  saveError.value = ''
  saveSuccess.value = false

  try {
    const reportData: ReportCreateRequest = {
      title: `${sourceKeyword.value} 分析报告`,
      platform: currentPlatform.value,
      source_keyword: sourceKeyword.value,
      time_from: parseTimeToTimestamp(timeFrom.value),
      time_to: parseTimeToTimestamp(timeTo.value),
      content: generatedReport.value,
      record_count: exportRecordCount.value,
    }

    await createReport(reportData)
    saveSuccess.value = true
    emit('saved')
  } catch (e: any) {
    console.error('Failed to save report:', e)
    saveError.value = e.message || '保存失败'
  } finally {
    saving.value = false
  }
}

function handleClose() {
  emit('close')
}

function handleBackdropClick(e: MouseEvent) {
  if ((e.target as HTMLElement).classList.contains('modal-backdrop')) {
    handleClose()
  }
}

function resetForm() {
  sourceKeyword.value = ''
  timeFrom.value = ''
  timeTo.value = ''
  generatedReport.value = ''
  keywordError.value = ''
  saveError.value = ''
  saveSuccess.value = false
  exportRecordCount.value = 0
  exportTruncated.value = false
  showKeywordDropdown.value = false
}

// Reset form when modal opens
watch(() => props.visible, (visible) => {
  if (visible) {
    resetForm()
    loadKeywords()
  }
})
</script>

<template>
  <Teleport to="body">
    <div
      v-if="visible"
      class="modal-backdrop"
      @click="handleBackdropClick"
    >
      <div class="modal-content">
        <div class="modal-header">
          <h3>📊 生成分析报告</h3>
          <button class="close-btn" @click="handleClose">✕</button>
        </div>
        
        <div class="modal-body">
          <!-- Configuration Section -->
          <div class="config-section">
            <div class="config-row">
              <div class="form-group keyword-group">
                <label>来源关键词 *</label>
                <div class="keyword-input-wrapper">
                  <input
                    v-model="sourceKeyword"
                    type="text"
                    placeholder="点击选择或输入关键词..."
                    :class="{ 'has-error': keywordError, 'is-valid': isKeywordValid }"
                    :disabled="generating"
                    @focus="handleKeywordFocus"
                    @blur="handleKeywordBlur"
                    @input="handleKeywordInput"
                  />
                  <span v-if="isKeywordValid" class="valid-icon">✓</span>
                  <div v-if="showKeywordDropdown && filteredKeywords.length > 0" class="keyword-suggestions">
                    <div v-if="loadingKeywords" class="keyword-loading">
                      加载中...
                    </div>
                    <template v-else>
                      <button
                        v-for="kw in filteredKeywords"
                        :key="kw"
                        type="button"
                        class="keyword-option"
                        :class="{ selected: kw === sourceKeyword }"
                        @mousedown.prevent="selectKeyword(kw)"
                      >
                        {{ kw }}
                      </button>
                      <div v-if="filteredKeywords.length === 0" class="keyword-empty">
                        无匹配关键词
                      </div>
                    </template>
                  </div>
                </div>
                <span v-if="keywordError" class="field-error">{{ keywordError }}</span>
                <span v-else-if="isValidating" class="field-hint field-validating">
                  ⏳ 验证关键词中...
                </span>
                <span v-else-if="loadingKeywords" class="field-hint">加载关键词中...</span>
                <span v-else-if="isKeywordValid" class="field-success">
                  ✓ 关键词有效
                </span>
                <span v-else class="field-hint">
                  共 {{ availableKeywords.length }} 个可用关键词
                  <template v-if="sourceKeyword && !isKeywordValid && filteredKeywords.length > 0">
                    · 请从下拉列表中选择
                  </template>
                </span>
              </div>
            </div>

            <div class="config-row time-range">
              <div class="form-group">
                <label>开始日期</label>
                <div class="date-input-wrapper">
                  <input
                    v-model="timeFrom"
                    type="date"
                    :disabled="generating"
                    class="date-input"
                  />
                  <span class="date-icon">📅</span>
                </div>
              </div>
              <div class="form-group">
                <label>结束日期</label>
                <div class="date-input-wrapper">
                  <input
                    v-model="timeTo"
                    type="date"
                    :disabled="generating"
                    class="date-input"
                  />
                  <span class="date-icon">📅</span>
                </div>
              </div>
            </div>

            <div class="generate-actions">
              <button
                class="btn-generate"
                :disabled="generating || !isKeywordValid || isValidating"
                @click="handleGenerate"
              >
                <span v-if="generating" class="loading-icon">⟳</span>
                <span v-else>🚀</span>
                {{ generating ? '生成中...' : '生成报告' }}
              </button>
              <span v-if="exportRecordCount > 0" class="record-info">
                分析 {{ exportRecordCount }} 条记录
                <span v-if="exportTruncated" class="truncated-warning">(已截断)</span>
              </span>
            </div>
          </div>

          <!-- Report Preview Section -->
          <div class="report-section">
            <div class="section-header">
              <h4>📝 报告预览</h4>
              <div v-if="generatedReport && !generating" class="save-actions">
                <span v-if="saveSuccess" class="save-success">✅ 已保存</span>
                <span v-if="saveError" class="save-error">{{ saveError }}</span>
                <button
                  class="btn-save"
                  :disabled="saving || saveSuccess"
                  @click="handleSave"
                >
                  {{ saving ? '保存中...' : '💾 保存报告' }}
                </button>
              </div>
            </div>
            
            <div ref="reportPreviewRef" class="report-preview">
              <div v-if="!generatedReport && !generating" class="empty-state">
                <div class="empty-icon">📋</div>
                <p>配置参数后点击"生成报告"</p>
              </div>
              
              <div v-if="generating && !generatedReport" class="loading-state">
                <div class="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <p>正在生成报告...</p>
              </div>
              
              <div v-if="generatedReport" class="report-content">
                <pre class="report-text">{{ generatedReport }}</pre>
                <div v-if="generating" class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.modal-content {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 16px;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6),
              0 0 40px rgba(99, 102, 241, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(99, 102, 241, 0.15);
  background: rgba(99, 102, 241, 0.05);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #e0e0e0;
}

.close-btn {
  padding: 0.5rem;
  background: transparent;
  border: none;
  color: #a0a0b0;
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #e0e0e0;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Config Section */
.config-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.config-row {
  display: flex;
  gap: 1rem;
}

.config-row.time-range {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.keyword-group {
  flex: 1;
}

.form-group label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: #a0a0b0;
}

.keyword-input-wrapper {
  position: relative;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(10, 10, 18, 0.7);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 8px;
  color: #e0e0e0;
  font-size: 0.9rem;
  transition: all 0.2s;
  color-scheme: dark;
}

.date-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.date-input {
  padding-right: 2.5rem !important;
  cursor: pointer;
}

.date-input::-webkit-calendar-picker-indicator {
  position: absolute;
  right: 0;
  top: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.date-icon {
  position: absolute;
  right: 0.75rem;
  pointer-events: none;
  font-size: 1.1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.form-group input.has-error {
  border-color: #ef4444;
}

.form-group input.is-valid {
  border-color: #10b981;
  padding-right: 2.5rem;
}

.form-group input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.valid-icon {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #10b981;
  font-weight: bold;
}

.keyword-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #1e1e2e;
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 8px;
  margin-top: 4px;
  max-height: 250px;
  overflow-y: auto;
  z-index: 100;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
}

.keyword-loading,
.keyword-empty {
  padding: 1rem;
  text-align: center;
  color: #6a6a80;
  font-size: 0.875rem;
}

.keyword-option {
  display: block;
  width: 100%;
  padding: 0.75rem 1rem;
  text-align: left;
  background: transparent;
  border: none;
  color: #c0c0c0;
  cursor: pointer;
  transition: background 0.15s;
  font-size: 0.9rem;
}

.keyword-option:hover {
  background: rgba(99, 102, 241, 0.15);
  color: #e0e0e0;
}

.keyword-option.selected {
  background: rgba(99, 102, 241, 0.25);
  color: #a78bfa;
}

.field-error {
  font-size: 0.75rem;
  color: #f87171;
}

.field-hint {
  font-size: 0.75rem;
  color: #6a6a80;
}

.field-hint.field-validating {
  color: #fbbf24;
}

.field-success {
  font-size: 0.75rem;
  color: #10b981;
}

.generate-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-top: 0.5rem;
}

.btn-generate {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
}

.btn-generate:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.loading-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.record-info {
  font-size: 0.85rem;
  color: #a0a0b0;
}

.truncated-warning {
  color: #fbbf24;
}

/* Report Section */
.report-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 300px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.section-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #c0c0c0;
}

.save-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.save-success {
  font-size: 0.85rem;
  color: #10b981;
}

.save-error {
  font-size: 0.85rem;
  color: #f87171;
}

.btn-save {
  padding: 0.5rem 1rem;
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 6px;
  color: #10b981;
  font-weight: 500;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save:hover:not(:disabled) {
  background: rgba(16, 185, 129, 0.25);
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.report-preview {
  flex: 1;
  background: rgba(10, 10, 18, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 12px;
  padding: 1.25rem;
  overflow-y: auto;
  min-height: 250px;
  max-height: 400px;
}

.empty-state,
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #6a6a80;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.loading-dots,
.typing-indicator {
  display: flex;
  gap: 0.3rem;
  margin-bottom: 0.5rem;
}

.loading-dots span,
.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #6366f1;
  border-radius: 50%;
  animation: bounce 1.4s ease-in-out infinite;
}

.loading-dots span:nth-child(2),
.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dots span:nth-child(3),
.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-6px); }
}

.report-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.report-text {
  margin: 0;
  font-family: inherit;
  font-size: 0.9rem;
  line-height: 1.7;
  color: #d0d0d0;
  white-space: pre-wrap;
  word-break: break-word;
}

.typing-indicator {
  margin-top: 0.75rem;
}

@media (max-width: 768px) {
  .modal-backdrop {
    padding: 1rem;
  }

  .config-row.time-range {
    grid-template-columns: 1fr;
  }

  .generate-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
}
</style>
