# Change: Add Coze Chat Integration

## Why

Enable users to interact with Coze AI bots through the application. This provides a simple chat interface that connects to Coze API using PAT (Personal Access Token) authentication with SSE streaming for real-time response display.

## What Changes

- Add new Django app `apps/coze/` for Coze API integration
- Add backend API endpoint for chat with SSE streaming response
- Add environment variables for Coze configuration (`COZE_PAT`, `COZE_BOT_ID`)
- Add new frontend page `/chat` with text input and streaming response display
- Add new route, API functions, and Vue components for chat functionality

## Impact

- Affected specs: New `coze-chat-api`, `coze-chat-frontend` capabilities
- Affected code:
  - `backend/apps/coze/` (new app)
  - `backend/config/urls.py` (register new router)
  - `backend/config/settings/base.py` (add Coze env vars)
  - `backend/requirements/base.txt` (no new deps, httpx already available)
  - `frontend/src/views/CozeChatView.vue` (new page)
  - `frontend/src/api/coze.ts` (new API)
  - `frontend/src/router/index.ts` (new route)

