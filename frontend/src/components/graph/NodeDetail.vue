<script setup lang="ts">
import { computed } from 'vue'
import type { GraphNode } from '@/types/graph'

const props = defineProps<{
  node: GraphNode | null
}>()

const emit = defineEmits<{
  close: []
}>()

const typeLabels = {
  Channel: '频道',
  Article: '文章',
  Tag: '标签'
}

const displayProperties = computed(() => {
  if (!props.node) return []

  const { properties, type } = props.node
  const items: { label: string; value: string }[] = []

  if (type === 'Article') {
    if (properties.title) items.push({ label: 'Title', value: String(properties.title) })
    if (properties.author) items.push({ label: 'Author', value: String(properties.author) })
    if (properties.pubTime) items.push({ label: 'Published', value: String(properties.pubTime) })
    if (properties.summary) items.push({ label: 'Summary', value: String(properties.summary) })
    if (properties.url) items.push({ label: 'URL', value: String(properties.url) })
  } else if (type === 'Channel') {
    if (properties.name) items.push({ label: 'Name', value: String(properties.name) })
    if (properties.desc) items.push({ label: 'Description', value: String(properties.desc) })
    if (properties.nodeId) items.push({ label: 'Node ID', value: String(properties.nodeId) })
  } else if (type === 'Tag') {
    if (properties.name) items.push({ label: 'Name', value: String(properties.name) })
    if (properties.tagId) items.push({ label: 'Tag ID', value: String(properties.tagId) })
  }

  return items
})
</script>

<template>
  <Transition name="slide">
    <aside v-if="node" class="node-detail">
      <header class="detail-header">
        <div class="node-type-badge" :class="node.type.toLowerCase()">
          {{ typeLabels[node.type] || node.type }}
        </div>
        <button class="close-btn" @click="emit('close')">×</button>
      </header>

      <h2 class="node-title">{{ node.label }}</h2>

      <div class="properties">
        <div v-for="prop in displayProperties" :key="prop.label" class="property-item">
          <span class="property-label">{{ prop.label }}</span>
          <span
            class="property-value"
            :class="{ 'is-url': prop.label === 'URL' }"
          >
            <a
              v-if="prop.label === 'URL'"
              :href="prop.value"
              target="_blank"
              rel="noopener"
            >
              Open Article →
            </a>
            <template v-else>{{ prop.value }}</template>
          </span>
        </div>
      </div>
    </aside>
  </Transition>
</template>

<style scoped>
.node-detail {
  position: absolute;
  top: 0;
  right: 0;
  width: 340px;
  height: 100%;
  background: linear-gradient(180deg, #1e1e2e 0%, #252538 100%);
  border-left: 1px solid #3d3d5c;
  padding: 1.5rem;
  overflow-y: auto;
  z-index: 10;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.node-type-badge {
  padding: 0.3rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.node-type-badge.channel {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.node-type-badge.article {
  background: rgba(99, 102, 241, 0.2);
  color: #8b5cf6;
}

.node-type-badge.tag {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.close-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #2d2d44;
  border: none;
  border-radius: 6px;
  color: #a0a0b0;
  font-size: 1.25rem;
  cursor: pointer;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #3d3d5c;
}

.node-title {
  margin: 0 0 1.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #e0e0e0;
  line-height: 1.4;
}

.properties {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.property-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.property-label {
  font-size: 0.7rem;
  color: #6a6a80;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.property-value {
  font-size: 0.9rem;
  color: #b0b0c0;
  line-height: 1.5;
  word-break: break-word;
}

.property-value.is-url a {
  color: #6366f1;
  text-decoration: none;
}

.property-value.is-url a:hover {
  text-decoration: underline;
}

/* Slide transition */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>

