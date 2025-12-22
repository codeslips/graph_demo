<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

const isGraphView = computed(() => route.name === 'graph' || route.name === 'media-graph')
</script>

<template>
  <div class="app-layout" :class="{ 'full-screen': isGraphView }">
    <nav v-if="!isGraphView" class="app-nav">
      <div class="nav-brand">
        <RouterLink to="/" class="brand-link">
          <span class="brand-icon">📰</span>
          <span class="brand-text">旅游分析平台</span>
        </RouterLink>
      </div>

      <div class="nav-links">
        <RouterLink to="/" class="nav-link" :class="{ active: route.name === 'home' }">
          <span class="nav-icon">🏠</span>
          <span class="nav-text">首页</span>
        </RouterLink>
        <RouterLink to="/tasks" class="nav-link" :class="{ active: route.name === 'tasks' }">
          <span class="nav-icon">📋</span>
          <span class="nav-text">任务</span>
        </RouterLink>
        <RouterLink to="/media" class="nav-link" :class="{ active: route.name === 'media' || route.name === 'media-detail' }">
          <span class="nav-icon">📊</span>
          <span class="nav-text">媒体数据</span>
        </RouterLink>
        <RouterLink to="/media-graph" class="nav-link" :class="{ active: route.name === 'media-graph' }">
          <span class="nav-icon">🕸️</span>
          <span class="nav-text">媒体图谱</span>
        </RouterLink>
        <RouterLink to="/reports" class="nav-link" :class="{ active: route.name === 'reports' || route.name === 'report-detail' }">
          <span class="nav-icon">📝</span>
          <span class="nav-text">报告列表</span>
        </RouterLink>
        <RouterLink to="/chat" class="nav-link" :class="{ active: route.name === 'chat' }">
          <span class="nav-icon">🤖</span>
          <span class="nav-text">AI 对话</span>
        </RouterLink>
        <RouterLink to="/tech-stack" class="nav-link" :class="{ active: route.name === 'tech-stack' }">
          <span class="nav-icon">🏗️</span>
          <span class="nav-text">技术架构</span>
        </RouterLink>
        <a href="https://github.com/codeslips/graph_demo" target="_blank" class="nav-link">
          <span class="nav-icon">🐙</span>
          <span class="nav-text">GitHub</span>
        </a>
      </div>
    </nav>

    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-layout.full-screen .app-nav {
  display: none;
}

.app-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  height: 64px;
  background: rgba(10, 10, 18, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand {
  display: flex;
  align-items: center;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
}

.brand-icon {
  font-size: 1.5rem;
}

.brand-text {
  font-size: 1.125rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--color-text-primary) 0%, var(--color-accent) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
}

.nav-links {
  display: flex;
  gap: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.nav-icon {
  font-size: 1.125rem;
}

.nav-link:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.nav-link.active {
  color: var(--color-accent);
  background: rgba(99, 102, 241, 0.1);
}

@media (max-width: 1024px) {
  .app-nav {
    padding: 0 1rem;
    height: auto;
    flex-direction: column;
    align-items: stretch;
  }

  .nav-brand {
    height: 64px;
    justify-content: center;
    border-bottom: 1px solid var(--color-border);
    margin-bottom: 0.5rem;
  }

  .nav-links {
    overflow-x: auto;
    padding-bottom: 0.75rem;
    gap: 0.25rem;
    justify-content: flex-start;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .nav-links::-webkit-scrollbar {
    display: none;
  }

  .nav-link {
    flex-shrink: 0;
    flex-direction: column;
    gap: 0.25rem;
    padding: 0.5rem 0.75rem;
    font-size: 0.75rem;
    min-width: 72px;
    text-align: center;
  }

  .nav-icon {
    font-size: 1.25rem;
  }
}

.app-main {
  flex: 1;
}
</style>
