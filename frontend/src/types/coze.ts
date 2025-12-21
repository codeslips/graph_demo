/**
 * Coze chat types.
 */

export interface ChatRequest {
  message: string
}

export interface ChatError {
  error: string
  detail?: string
}

export interface CozeEvent {
  event: string
  data: string
}

export interface MessageDelta {
  type: string
  content: string
}

