<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

const isGraphView = computed(() => route.name === 'graph')
</script>

<template>
  <div class="app-layout" :class="{ 'full-screen': isGraphView }">
    <nav v-if="!isGraphView" class="app-nav">
      <div class="nav-brand">
        <RouterLink to="/" class="brand-link">
          <span class="brand-icon">📰</span>
          <span class="brand-text">澎湃图谱</span>
        </RouterLink>
      </div>

      <div class="nav-links">
        <RouterLink to="/" class="nav-link" :class="{ active: route.name === 'home' }">
          首页
        </RouterLink>
        <RouterLink to="/tasks" class="nav-link" :class="{ active: route.name === 'tasks' }">
          任务
        </RouterLink>
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
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.nav-link:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.nav-link.active {
  color: var(--color-accent);
  background: rgba(99, 102, 241, 0.1);
}

.app-main {
  flex: 1;
}
</style>
