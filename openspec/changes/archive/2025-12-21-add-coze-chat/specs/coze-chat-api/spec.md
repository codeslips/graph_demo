# Coze Chat API

Backend API for Coze AI chat integration with SSE streaming support.

## ADDED Requirements

### Requirement: Coze Configuration

The system SHALL read Coze configuration from environment variables:
- `COZE_PAT`: Personal Access Token for authentication (required)
- `COZE_BOT_ID`: The bot ID to chat with (required)
- `COZE_API_BASE_URL`: API base URL (optional, defaults to `https://api.coze.cn`)

#### Scenario: Configuration loaded on startup
- **WHEN** the Django application starts
- **THEN** Coze configuration values are loaded from environment variables
- **AND** the values are accessible via Django settings

#### Scenario: Missing required configuration
- **WHEN** `COZE_PAT` or `COZE_BOT_ID` is not set
- **AND** a chat request is made
- **THEN** the API returns a 500 error with message indicating missing configuration

### Requirement: Chat Endpoint

The system SHALL provide a POST endpoint at `/api/v1/coze/chat` that accepts a message and returns SSE streaming response from Coze.

#### Scenario: Successful chat request with streaming
- **WHEN** a POST request is made to `/api/v1/coze/chat` with body `{"message": "你好"}`
- **THEN** the response Content-Type is `text/event-stream`
- **AND** the response streams SSE events from Coze API
- **AND** events include `conversation.message.delta` with partial content
- **AND** events include `conversation.message.completed` with full response
- **AND** a final `done` event indicates completion

#### Scenario: Empty message validation
- **WHEN** a POST request is made with empty or missing message
- **THEN** the API returns 400 Bad Request with error message

#### Scenario: Coze API error handling
- **WHEN** the Coze API returns an error
- **THEN** the API returns the error as an SSE event with type "error"
- **AND** includes the error message for user display

### Requirement: Auto-generated User ID

The system SHALL generate a unique user ID (UUID) for each chat request to identify the conversation with Coze.

#### Scenario: User ID generation
- **WHEN** a chat request is processed
- **THEN** a new UUID is generated as the user_id
- **AND** this user_id is sent to Coze API in the request body

### Requirement: SSE Response Forwarding

The system SHALL forward SSE events from Coze API to the client in real-time using Django's StreamingHttpResponse.

#### Scenario: Real-time streaming
- **WHEN** Coze API sends SSE events
- **THEN** each event is immediately forwarded to the client
- **AND** the connection remains open until Coze completes the response

#### Scenario: Connection timeout
- **WHEN** the Coze API does not respond within 60 seconds
- **THEN** the connection is closed
- **AND** an error event is sent to the client

