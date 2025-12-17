# Frontend Style Specifications

## ADDED Requirements

### Requirement: Modern Navigation Bar
The navigation bar in `App.vue` MUST feature a modern, concise design.

#### Scenario: Visual Appearance
-   **Given** the user is viewing the application
-   **When** they look at the navigation bar
-   **Then** it should use the project's color palette variables.
-   **And** it should have a subtle bottom border.
-   **And** the background should blend well with the dark theme (e.g., subtle gradient or solid color with blur).

#### Scenario: Navigation Links
-   **Given** the user interacts with navigation links
-   **When** they hover over a link
-   **Then** the background and text color should change smoothly (transition).
-   **When** a link is active
-   **Then** it should be clearly distinguishable (e.g., different background or text color).

### Requirement: Brand Identity
The brand text "ThePaper Graph" MUST maintain its gradient style but be refined for legibility and modern aesthetics.

#### Scenario: Brand Display
-   **Given** the navigation bar
-   **When** displaying the brand
-   **Then** the icon and text should be aligned vertically center.
-   **And** the text should use a gradient that matches the theme accents (`--color-accent`, etc.).
