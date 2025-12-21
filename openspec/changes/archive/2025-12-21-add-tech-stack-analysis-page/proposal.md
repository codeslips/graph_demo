# Change: Add Tech Stack Analysis Page

## Why

Users and developers need a clear understanding of the platform's architecture and the technologies being used. A dedicated "Tech Stack Analysis" page will provide a visual and textual breakdown of the system components, based on the project's `README.md`, making it easier for stakeholders to grasp the system's capabilities and design.

## What Changes

- **New View**: Create `TechStackView.vue` which includes:
  - Visual system architecture diagram.
  - Detailed breakdown of each layer (Backend, Frontend, Database, AI, etc.).
  - Key features and technologies used in each layer.
- **Routing**: Add `/tech-stack` route to the frontend router.
- **Navigation**: Add a link to the new page in the home page's tech stack footer and potentially the sidebar/header.

## Impact

- **Affected code**: 
  - `frontend/src/views/TechStackView.vue` (new file)
  - `frontend/src/router/index.ts`
  - `frontend/src/views/HomeView.vue`

