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
          <span class="brand-text">ThePaper Graph</span>
        </RouterLink>
      </div>

      <div class="nav-links">
        <RouterLink to="/" class="nav-link" :class="{ active: route.name === 'home' }">
          Home
        </RouterLink>
        <RouterLink to="/tasks" class="nav-link" :class="{ active: route.name === 'tasks' }">
          Tasks
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
  height: 60px;
  background: linear-gradient(180deg, #12121a 0%, #0a0a12 100%);
  border-bottom: 1px solid #2d2d44;
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
  font-size: 1.1rem;
  font-weight: 700;
  background: linear-gradient(135deg, #e0e0e0 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  gap: 0.5rem;
}

.nav-link {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #a0a0b0;
  text-decoration: none;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: #e0e0e0;
  background: #1e1e2e;
}

.nav-link.active {
  color: #e0e0e0;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
}

.app-main {
  flex: 1;
}
</style>
