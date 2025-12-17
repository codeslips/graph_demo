<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <header>
      <h1>ThePaper Graph</h1>
      <p>澎湃新闻 Web Crawl → Graph Insight Demo</p>
    </header>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
}

header {
  text-align: center;
  margin-bottom: 2rem;
}

header h1 {
  font-size: 2.5rem;
  color: #1a1a1a;
}

header p {
  color: #666;
  margin-top: 0.5rem;
}
</style>

