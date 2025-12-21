<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { sendChatMessage } from '@/api/coze'

const message = ref('')
const response = ref('')
const isLoading = ref(false)
const error = ref('')
const responseAreaRef = ref<HTMLDivElement | null>(null)

async function handleSend() {
  if (!message.value.trim() || isLoading.value) return

  const userMessage = message.value.trim()
  message.value = ''
  response.value = ''
  error.value = ''
  isLoading.value = true

  await sendChatMessage(
    { message: userMessage },
    {
      onMessage: (content: string) => {
        response.value += content
        scrollToBottom()
      },
      onError: (err: string) => {
        error.value = err
        isLoading.value = false
      },
      onComplete: () => {
        isLoading.value = false
      }
    }
  )
}

function scrollToBottom() {
  nextTick(() => {
    if (responseAreaRef.value) {
      responseAreaRef.value.scrollTop = responseAreaRef.value.scrollHeight
    }
  })
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}
</script>

<template>
  <div class="chat-view">
    <div class="chat-header">
      <div class="header-content">
        <span class="header-icon">🤖</span>
        <div>
          <h1>AI 对话助手</h1>
          <p class="header-subtitle">与 Coze AI 进行对话</p>
        </div>
      </div>
    </div>

    <div class="chat-container">
      <!-- Response Area -->
      <div class="response-area" ref="responseAreaRef">
        <div v-if="!response && !isLoading && !error" class="empty-state">
          <div class="empty-icon">💬</div>
          <p>输入消息开始对话</p>
        </div>

        <div v-if="isLoading && !response" class="loading-state">
          <div class="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <p>正在思考中...</p>
        </div>

        <div v-if="response" class="response-content">
          <div class="response-label">
            <span class="label-icon">🤖</span>
            AI 回复
          </div>
          <div class="response-text">{{ response }}</div>
          <div v-if="isLoading" class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>

        <div v-if="error" class="error-state">
          <div class="error-icon">⚠️</div>
          <p class="error-title">出错了</p>
          <p class="error-message">{{ error }}</p>
        </div>
      </div>

      <!-- Input Area -->
      <div class="input-area">
        <div class="input-wrapper">
          <textarea
            v-model="message"
            @keydown="handleKeydown"
            placeholder="输入您的问题..."
            :disabled="isLoading"
            rows="1"
            class="message-input"
          ></textarea>
          <button
            @click="handleSend"
            :disabled="!message.trim() || isLoading"
            class="send-button"
          >
            <span v-if="isLoading" class="button-loading"></span>
            <span v-else>发送</span>
          </button>
        </div>
        <p class="input-hint">按 Enter 发送，Shift + Enter 换行</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-view {
  min-height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, #0a0a12 0%, #12121a 100%);
}

/* Header */
.chat-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--color-border);
  background: linear-gradient(90deg, rgba(99, 102, 241, 0.05) 0%, transparent 100%);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  max-width: 900px;
  margin: 0 auto;
}

.header-icon {
  font-size: 2.5rem;
}

.chat-header h1 {
  font-size: 1.5rem;
  background: linear-gradient(135deg, #e0e0e0 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-subtitle {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  margin-top: 0.25rem;
}

/* Chat Container */
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
  gap: 1.5rem;
}

/* Response Area */
.response-area {
  flex: 1;
  min-height: 300px;
  max-height: 60vh;
  overflow-y: auto;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
}

.empty-state,
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: var(--color-text-muted);
}

.empty-icon,
.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* Loading Animation */
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
  background: var(--color-accent);
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
  0%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-6px);
  }
}

/* Response Content */
.response-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.response-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--color-accent);
  margin-bottom: 0.75rem;
  font-weight: 500;
}

.label-icon {
  font-size: 1.1rem;
}

.response-text {
  font-size: 1rem;
  line-height: 1.8;
  color: var(--color-text-primary);
  white-space: pre-wrap;
  word-break: break-word;
}

.typing-indicator {
  margin-top: 0.75rem;
}

/* Error State */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
}

.error-title {
  font-weight: 600;
  color: var(--color-error);
  margin-bottom: 0.5rem;
}

.error-message {
  color: var(--color-text-secondary);
  font-size: 0.9rem;
}

/* Input Area */
.input-area {
  flex-shrink: 0;
}

.input-wrapper {
  display: flex;
  gap: 0.75rem;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 0.75rem;
  transition: border-color var(--transition-fast);
}

.input-wrapper:focus-within {
  border-color: var(--color-accent);
}

.message-input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--color-text-primary);
  font-size: 1rem;
  line-height: 1.5;
  resize: none;
  min-height: 24px;
  max-height: 120px;
  padding: 0.5rem;
}

.message-input::placeholder {
  color: var(--color-text-muted);
}

.message-input:focus {
  outline: none;
}

.message-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.send-button {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  padding: 0.75rem 1.25rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 0.95rem;
  transition: all var(--transition-fast);
}

.send-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.button-loading {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.input-hint {
  text-align: center;
  font-size: 0.8rem;
  color: var(--color-text-muted);
  margin-top: 0.75rem;
}

/* Responsive */
@media (max-width: 768px) {
  .chat-container {
    padding: 1rem;
  }

  .response-area {
    min-height: 200px;
  }

  .input-wrapper {
    flex-direction: column;
  }

  .send-button {
    width: 100%;
  }
}
</style>

