## Context

The project has an external media crawl service running separately (e.g., at `http://127.0.0.1:8777`) that handles the actual crawling of social media platforms. This service has its own API:
- `POST /api/crawler/start` - Start a crawl task
- `GET /api/crawler/status` - Check task status

The backend needs to act as a proxy to this service, and the frontend needs to provide a UI for users to configure and trigger crawl tasks.

**Key constraint**: Only one crawl task can run at a time. The UI must prevent users from triggering multiple concurrent tasks.

## Goals / Non-Goals

**Goals:**
- Allow users to trigger crawl tasks from the frontend
- Proxy requests through our backend (for security and configuration)
- Provide status monitoring with automatic polling
- Support all crawl parameters (platform, login_type, crawler_type, keywords, etc.)
- Notify users when crawl completes
- Prevent multiple concurrent tasks

**Non-Goals:**
- Managing crawl history (external service handles this)
- Automatic data sync after crawl (external service writes directly to shared DB)
- Advanced authentication with external service (simple URL-based connection)

## Decisions

### Decision 1: Backend Proxy Pattern
**What**: Backend proxies requests to external crawler service rather than frontend calling directly.
**Why**: 
- Keeps external service URL private (only in backend env)
- Allows for future authentication/rate limiting
- Consistent with existing API patterns

### Decision 2: Environment Variable Configuration
**What**: Use `MEDIA_CRAWL_SERVICE_URL` environment variable
**Why**: Standard pattern for external service configuration, matches existing env var patterns in settings/base.py

### Decision 3: Status Polling vs WebSocket
**What**: Use polling (every 2-3 seconds) instead of WebSocket
**Why**:
- Simpler implementation
- Status checks are infrequent
- Matches existing polling pattern for Neo4j sync status
- External service doesn't support WebSocket

### Decision 4: Single Task Constraint via Status Check
**What**: Before allowing task creation, frontend checks current status
**Why**:
- Simple to implement
- Prevents race conditions at UI level
- Backend status endpoint is the source of truth

## Risks / Trade-offs

- **External service unavailable** → Show clear error message, disable form
- **Polling overhead** → 2-3s interval is acceptable, stop polling when idle
- **Status desync** → Always fetch fresh status before operations

## Open Questions

None - all clarified with user.

