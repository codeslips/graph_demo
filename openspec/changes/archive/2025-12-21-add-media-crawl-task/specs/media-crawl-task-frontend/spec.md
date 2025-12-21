## ADDED Requirements

### Requirement: Media Crawl Task Page
The system SHALL provide a dedicated page for managing media crawl tasks.

#### Scenario: Page accessible via route
- **WHEN** the user navigates to `/media/crawl`
- **THEN** the Media Crawl Task page SHALL be displayed

#### Scenario: Navigation link available
- **WHEN** the user is on the Media View page
- **THEN** a link/button to navigate to the crawl task page SHALL be visible

### Requirement: Crawl Task Form
The system SHALL provide a form to configure and start new crawl tasks.

#### Scenario: Display form fields
- **WHEN** the user views the crawl task page
- **THEN** the form SHALL display input fields for:
  - Platform (dropdown: xhs, douyin, bilibili, kuaishou, weibo, tieba, zhihu)
  - Login Type (dropdown: qrcode, cookie)
  - Crawler Type (dropdown: search, detail, creator)
  - Keywords (text input)
  - Specified IDs (text input)
  - Creator IDs (text input)
  - Start Page (number input)
  - Enable Comments (checkbox)
  - Enable Sub-Comments (checkbox)
  - Cookies (textarea)
  - Headless Mode (checkbox)

#### Scenario: Submit form
- **WHEN** the user fills in required fields and clicks submit
- **AND** no crawler task is currently running
- **THEN** a new crawler task SHALL be started via the API

### Requirement: Single Task Constraint
The system SHALL prevent users from starting multiple concurrent crawl tasks.

#### Scenario: Check status before submit
- **WHEN** the user attempts to start a new task
- **THEN** the system SHALL first check the current crawler status

#### Scenario: Block when task running
- **WHEN** a crawler task is already running (status = "running")
- **THEN** the submit button SHALL be disabled
- **AND** a message SHALL indicate that a task is in progress

#### Scenario: Allow when idle
- **WHEN** no crawler task is running (status = "idle")
- **THEN** the submit button SHALL be enabled

### Requirement: Status Display
The system SHALL display the current crawler task status.

#### Scenario: Show running status
- **WHEN** a crawler task is running
- **THEN** the page SHALL display:
  - Status indicator (running)
  - Current platform being crawled
  - Crawler type
  - Start time
  - Loading animation

#### Scenario: Show idle status
- **WHEN** no crawler task is running
- **THEN** the page SHALL display idle status

#### Scenario: Show error status
- **WHEN** the last crawler task failed
- **THEN** the error message SHALL be displayed

### Requirement: Status Polling
The system SHALL automatically poll for status updates while a task is running.

#### Scenario: Poll while running
- **WHEN** a crawler task is running
- **THEN** the system SHALL poll status every 2-3 seconds

#### Scenario: Stop polling when idle
- **WHEN** the crawler task completes (status changes to "idle")
- **THEN** the system SHALL stop polling
- **AND** a completion notification SHALL be shown

### Requirement: Completion Notification
The system SHALL notify users when a crawl task completes.

#### Scenario: Task completes successfully
- **WHEN** the crawler status changes from "running" to "idle"
- **AND** no error_message is present
- **THEN** a success notification SHALL be displayed

#### Scenario: Task fails
- **WHEN** the crawler status changes to "idle"
- **AND** an error_message is present
- **THEN** an error notification SHALL be displayed with the error message

### Requirement: Loading States
The system SHALL display appropriate loading indicators.

#### Scenario: Starting task loading
- **WHEN** the user clicks submit to start a task
- **THEN** the submit button SHALL show a loading state
- **AND** be disabled until the request completes

#### Scenario: Initial page loading
- **WHEN** the page first loads
- **THEN** a loading indicator SHALL be shown while fetching initial status

### Requirement: Error Handling
The system SHALL handle errors gracefully.

#### Scenario: Service unavailable
- **WHEN** the crawler service is not reachable
- **THEN** an error message SHALL be displayed
- **AND** the form SHALL be disabled

#### Scenario: API error
- **WHEN** an API request fails
- **THEN** the error message SHALL be displayed to the user

