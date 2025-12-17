<script setup lang="ts">
// Home view - dashboard placeholder
</script>

<template>
  <div class="home">
    <h2>Dashboard</h2>
    <p>Welcome to ThePaper Graph. Start by creating a crawl task.</p>
    <div class="quick-actions">
      <router-link to="/tasks" class="btn">View Tasks</router-link>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
}

.quick-actions {
  margin-top: 2rem;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: #1a1a1a;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.btn:hover {
  background: #333;
}
</style>

