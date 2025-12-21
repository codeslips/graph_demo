# Change: Localize Frontend to Chinese

## Why
The user requested that the site use Chinese as the default language. Since the target data source is "ThePaper" (澎湃新闻), a Chinese news site, having a Chinese interface improves usability and consistency.

## What Changes
- Update `index.html` lang attribute to `zh-CN`.
- Translate static text in `App.vue`, `HomeView.vue`, `TaskForm.vue`, `TaskListView.vue`, `TaskDetailView.vue`, `GraphView.vue` and related components to Simplified Chinese.
- Update page title to "旅游分析平台" (ThePaper Graph).

## Impact
- Affected specs: `localization` (new).
- Affected code: `frontend/index.html`, `frontend/src/**/*.vue`.

