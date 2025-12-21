## Context

Integrate Coze AI chat capability into the application. Coze provides a chat API at `https://api.coze.cn/v3/chat` that supports both streaming and non-streaming responses. We use PAT (Personal Access Token) for authentication as specified for testing/demo environments.

### Stakeholders
- End users who want to chat with the Coze bot
- Developers maintaining the integration

### Constraints
- PAT token and Bot ID must be configured via environment variables
- Each request creates a new conversation (no session persistence)
- User ID is auto-generated per request

## Goals / Non-Goals

### Goals
- Simple chat API endpoint that proxies to Coze with SSE streaming
- Frontend page with text input and real-time response display
- Basic error handling with user-visible error messages

### Non-Goals
- User authentication/authorization (demo mode)
- Conversation history persistence
- Multi-turn conversation support
- File/image uploads
- Custom bot configuration UI

## Decisions

### Decision: Use SSE for Streaming
Use Server-Sent Events (SSE) to stream Coze responses to the frontend.
- **Why**: Coze API supports streaming via SSE, and it provides better UX with real-time character-by-character display
- **Alternatives**: WebSocket (overkill for unidirectional streaming), polling (poor UX)

### Decision: Generate Random User ID
Generate a UUID for each chat request as the user_id.
- **Why**: Simplest approach for demo; no user auth needed
- **Alternatives**: Fixed demo user ID (could cause rate limiting issues)

### Decision: New Django App `apps/coze/`
Create a dedicated app for Coze integration.
- **Why**: Follows existing project pattern (apps/crawl/, apps/graph/, apps/media_crawl/)
- **Alternatives**: Add to existing app (breaks single-responsibility)

### Decision: Django Ninja with StreamingHttpResponse
Use Django's `StreamingHttpResponse` to forward SSE from Coze API.
- **Why**: Django Ninja supports streaming responses; httpx supports streaming requests
- **Alternatives**: Celery task (unnecessary complexity for simple streaming)

## Data Flow

```
Frontend                 Backend                   Coze API
   |                        |                          |
   |-- POST /chat --------->|                          |
   |                        |-- POST /v3/chat -------->|
   |                        |   (stream=true)          |
   |                        |                          |
   |<-- SSE events ---------|<-- SSE events -----------|
   |                        |                          |
   |-- (render text) -------|                          |
```

## API Design

### Backend Endpoint
```
POST /api/v1/coze/chat
Content-Type: application/json

Request:
{
  "message": "用户输入的消息"
}

Response: text/event-stream (SSE)
event: conversation.message.delta
data: {"type": "answer", "content": "部分回复..."}

event: conversation.message.completed
data: {"type": "answer", "content": "完整回复"}

event: done
data: [DONE]
```

## Environment Variables

```
COZE_PAT=pat_xxxxxxxxxxxx
COZE_BOT_ID=7xxxxxxxxxxxxxxxxxx
COZE_API_BASE_URL=https://api.coze.cn  # optional, defaults to this
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| PAT token exposure | Store in env vars, never log or expose to frontend |
| Coze API rate limiting | Add basic retry with backoff; show user-friendly error |
| Network timeout | Set reasonable timeout (60s for streaming); handle gracefully |
| Invalid bot_id | Validate on startup or first request; clear error message |

## Open Questions

None - scope is well-defined for demo purposes.

