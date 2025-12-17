<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const taskId = route.params.id
</script>

<template>
  <div class="task-detail">
    <h2>Task Detail</h2>
    <p>Viewing task: {{ taskId }}</p>
  </div>
</template>

<style scoped>
.task-detail {
  padding: 1rem;
}
</style>

