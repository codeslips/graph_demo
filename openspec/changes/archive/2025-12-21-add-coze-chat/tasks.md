## 1. Backend Implementation

- [x] 1.1 Add Coze configuration to `backend/config/settings/base.py` (COZE_PAT, COZE_BOT_ID, COZE_API_BASE_URL)
- [x] 1.2 Create `backend/apps/coze/` app structure (__init__.py, apps.py, api.py, schemas.py, services.py)
- [x] 1.3 Implement Coze API service in `services.py` (HTTP client for Coze API with SSE streaming)
- [x] 1.4 Implement chat endpoint in `api.py` with StreamingHttpResponse for SSE
- [x] 1.5 Register coze router in `backend/config/urls.py`
- [x] 1.6 Add `apps.coze` to INSTALLED_APPS in settings

## 2. Frontend Implementation

- [x] 2.1 Create `frontend/src/api/coze.ts` for chat API with EventSource/fetch streaming
- [x] 2.2 Create `frontend/src/types/coze.ts` for TypeScript types
- [x] 2.3 Create `frontend/src/views/CozeChatView.vue` with chat UI (input + response area)
- [x] 2.4 Add `/chat` route to `frontend/src/router/index.ts`
- [x] 2.5 Add navigation link to chat page in sidebar/header

## 3. Documentation & Configuration

- [x] 3.1 Update docker-compose environment variables with COZE_* placeholders
