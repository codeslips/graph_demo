/**
 * Coze chat API client with SSE streaming support.
 */

import type { ChatRequest } from '@/types/coze'

const API_BASE = '/api/v1'

export interface StreamCallbacks {
  onMessage: (content: string) => void
  onError: (error: string) => void
  onComplete: () => void
}

/**
 * Send a chat message and handle streaming response.
 */
export async function sendChatMessage(
  request: ChatRequest,
  callbacks: StreamCallbacks
): Promise<void> {
  const controller = new AbortController()

  try {
    const response = await fetch(`${API_BASE}/coze/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request),
      signal: controller.signal
    })

    if (!response.ok) {
      const errorData = await response.json()
      callbacks.onError(errorData.detail || errorData.error || 'Request failed')
      return
    }

    const reader = response.body?.getReader()
    if (!reader) {
      callbacks.onError('No response body')
      return
    }

    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })

      // Process complete SSE events
      const lines = buffer.split('\n')
      buffer = lines.pop() || '' // Keep incomplete line in buffer

      let currentEvent = ''
      let currentData = ''

      for (const line of lines) {
        if (line.startsWith('event:')) {
          currentEvent = line.slice(6).trim()
        } else if (line.startsWith('data:')) {
          currentData = line.slice(5).trim()
        } else if (line === '' && currentData) {
          // End of event, process it
          processEvent(currentEvent, currentData, callbacks)
          currentEvent = ''
          currentData = ''
        }
      }
    }

    callbacks.onComplete()
  } catch (error) {
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        callbacks.onComplete()
      } else {
        callbacks.onError(error.message)
      }
    } else {
      callbacks.onError('Unknown error occurred')
    }
  }
}

function processEvent(event: string, data: string, callbacks: StreamCallbacks): void {
  if (event === 'error') {
    try {
      const errorData = JSON.parse(data)
      callbacks.onError(errorData.detail || errorData.error || 'Unknown error')
    } catch {
      callbacks.onError(data)
    }
    return
  }

  if (event === 'done' || data === '[DONE]') {
    callbacks.onComplete()
    return
  }

  // Handle conversation.message.delta events
  if (event === 'conversation.message.delta') {
    try {
      const messageData = JSON.parse(data)
      if (messageData.type === 'answer' && messageData.content) {
        callbacks.onMessage(messageData.content)
      }
    } catch {
      // Ignore parse errors for delta events
    }
  }
}

