<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const graphId = route.params.id
</script>

<template>
  <div class="graph-view">
    <h2>Graph Visualization</h2>
    <p>Graph for task: {{ graphId }}</p>
    <div class="graph-canvas">
      <!-- Graph visualization will be rendered here -->
    </div>
  </div>
</template>

<style scoped>
.graph-view {
  padding: 1rem;
}

.graph-canvas {
  width: 100%;
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-top: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
}
</style>

