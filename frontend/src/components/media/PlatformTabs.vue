<script setup lang="ts">
import { computed } from 'vue'
import { useMediaStore, PLATFORM_CONFIGS } from '@/stores/media'
import type { Platform } from '@/types/media'

const mediaStore = useMediaStore()

const platforms = computed(() => PLATFORM_CONFIGS)

function handlePlatformChange(platform: Platform) {
  mediaStore.setPlatform(platform)
}

function handleEntityChange(entityId: string) {
  mediaStore.setEntity(entityId)
}
</script>

<template>
  <div class="platform-tabs">
    <!-- Platform selector -->
    <div class="platform-selector">
      <button
        v-for="platform in platforms"
        :key="platform.id"
        class="platform-btn"
        :class="{ active: mediaStore.currentPlatform === platform.id }"
        @click="handlePlatformChange(platform.id)"
      >
        <span class="platform-icon">{{ platform.icon }}</span>
        <span class="platform-name">{{ platform.name }}</span>
      </button>
    </div>
    
    <!-- Entity tabs -->
    <div v-if="mediaStore.currentPlatformConfig" class="entity-tabs">
      <button
        v-for="entity in mediaStore.currentPlatformConfig.entities"
        :key="entity.id"
        class="entity-tab"
        :class="{ active: mediaStore.currentEntityId === entity.id }"
        @click="handleEntityChange(entity.id)"
      >
        {{ entity.name }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.platform-tabs {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.platform-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.5rem;
  background: rgba(30, 30, 46, 0.5);
  border-radius: 12px;
  border: 1px solid var(--color-border, #3d3d5c);
}

.platform-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 8px;
  color: var(--color-text-secondary, #a0a0b0);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
}

.platform-btn:hover {
  background: rgba(99, 102, 241, 0.1);
  color: var(--color-text-primary, #e0e0e0);
}

.platform-btn.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
  border-color: rgba(99, 102, 241, 0.4);
  color: var(--color-accent, #6366f1);
}

.platform-icon {
  font-size: 1.125rem;
}

.platform-name {
  white-space: nowrap;
}

.entity-tabs {
  display: flex;
  gap: 0.25rem;
  padding: 0.25rem;
  background: rgba(30, 30, 46, 0.3);
  border-radius: 8px;
  border: 1px solid var(--color-border, #3d3d5c);
}

.entity-tab {
  padding: 0.5rem 1rem;
  background: transparent;
  border: none;
  border-radius: 6px;
  color: var(--color-text-secondary, #a0a0b0);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.8125rem;
  font-weight: 500;
}

.entity-tab:hover {
  color: var(--color-text-primary, #e0e0e0);
  background: rgba(255, 255, 255, 0.05);
}

.entity-tab.active {
  background: rgba(99, 102, 241, 0.15);
  color: var(--color-accent, #6366f1);
}

@media (max-width: 768px) {
  .platform-selector {
    overflow-x: auto;
    flex-wrap: nowrap;
    -webkit-overflow-scrolling: touch;
  }
  
  .platform-btn {
    flex-shrink: 0;
  }
}
</style>

