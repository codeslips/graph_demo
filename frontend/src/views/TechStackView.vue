<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const techStack = [
  {
    category: 'Backend',
    icon: '⚙️',
    techs: [
      { name: 'Django 5.x', desc: 'Powerful Python web framework for core logic' },
      { name: 'Django Ninja', desc: 'Fast, type-safe API framework with OpenAPI support' },
      { name: 'Python 3.11+', desc: 'Robust and flexible programming language' }
    ]
  },
  {
    category: 'Frontend',
    icon: '🎨',
    techs: [
      { name: 'Vue 3', desc: 'Modern composition API based reactive framework' },
      { name: 'Vite', desc: 'Next-generation ultra-fast frontend tooling' },
      { name: 'TypeScript', desc: 'Type-safe development for complex frontend logic' },
      { name: 'ECharts', desc: 'Powerful interactive data visualization' }
    ]
  },
  {
    category: 'Database & Storage',
    icon: '💾',
    techs: [
      { name: 'PostgreSQL 15+', desc: 'Primary relational database for structured data' },
      { name: 'Neo4j 5.x', desc: 'Graph database for complex relationship mapping' },
      { name: 'Redis 7.x', desc: 'High-performance cache and message broker' }
    ]
  },
  {
    category: 'Task & Queue',
    icon: '⚡',
    techs: [
      { name: 'Celery 5.x', desc: 'Distributed task queue for asynchronous processing' },
      { name: 'Redis', desc: 'Message broker for Celery tasks' }
    ]
  },
  {
    category: 'AI & Analysis',
    icon: '🤖',
    techs: [
      { name: 'Coze AI', desc: 'Intelligent content analysis and entity extraction' },
      { name: 'Natural Language Processing', desc: 'Custom extractors for travel-specific data' }
    ]
  },
  {
    category: 'Infrastructure',
    icon: '🐳',
    techs: [
      { name: 'Docker', desc: 'Containerization for consistent environments' },
      { name: 'Docker Compose', desc: 'Multi-container orchestration for local/prod' },
      { name: 'Nginx', desc: 'High-performance reverse proxy and static server' }
    ]
  }
]

function goBack() {
  router.back()
}
</script>

<template>
  <div class="tech-stack-view">
    <header class="page-header">
      <button class="back-btn" @click="goBack">
        <span class="icon">←</span> 返回
      </button>
      <div class="header-content">
        <h1 class="title">技术栈分析</h1>
        <p class="subtitle">Media Travel Data Analysis Platform Architecture & Tech Stack</p>
      </div>
    </header>

    <main class="content">
      <!-- Architecture Overview -->
      <section class="architecture-section">
        <div class="section-card architecture-card">
          <h2 class="card-title">系统架构概览</h2>
          <div class="architecture-diagram">
            <div class="layer client-layer">
              <div class="node frontend">Vue 3 Frontend</div>
            </div>
            <div class="connector">⇅</div>
            <div class="layer api-layer">
              <div class="node backend">Django Ninja API</div>
            </div>
            <div class="connector">⇅</div>
            <div class="layer storage-layer">
              <div class="node-group">
                <div class="node postgres">PostgreSQL</div>
                <div class="node neo4j">Neo4j</div>
                <div class="node redis">Redis</div>
              </div>
            </div>
            <div class="worker-path">
              <div class="node worker">Celery Workers</div>
              <div class="node coze">Coze AI</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Detailed Tech Grid -->
      <section class="tech-details-section">
        <div v-for="group in techStack" :key="group.category" class="tech-group-card">
          <div class="group-header">
            <span class="group-icon">{{ group.icon }}</span>
            <h2 class="group-title">{{ group.category }}</h2>
          </div>
          <div class="tech-list">
            <div v-for="tech in group.techs" :key="tech.name" class="tech-item">
              <h3 class="tech-name">{{ tech.name }}</h3>
              <p class="tech-desc">{{ tech.desc }}</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.tech-stack-view {
  min-height: calc(100vh - 60px);
  padding: 2rem;
  background: #0a0a0f;
  color: #e2e8f0;
}

.page-header {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  margin-bottom: 3rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #fff;
  border-color: #6366f1;
}

.title {
  font-size: 2.25rem;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  color: #64748b;
  margin-top: 0.5rem;
}

.content {
  max-width: 1200px;
  margin: 0 auto;
}

/* Architecture Card */
.architecture-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  padding: 2.5rem;
  margin-bottom: 3rem;
  backdrop-filter: blur(12px);
}

.card-title {
  font-size: 1.5rem;
  margin-bottom: 2.5rem;
  text-align: center;
  color: #f1f5f9;
}

.architecture-diagram {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.layer {
  width: 100%;
  display: flex;
  justify-content: center;
}

.node {
  padding: 1rem 2rem;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 12px;
  font-weight: 600;
  color: #a5b4fc;
}

.node-group {
  display: flex;
  gap: 1.5rem;
}

.connector {
  font-size: 1.5rem;
  color: #475569;
}

.worker-path {
  margin-top: 2rem;
  display: flex;
  gap: 2rem;
  position: relative;
  padding-top: 2rem;
  border-top: 1px dashed #475569;
}

.worker-path::before {
  content: 'Async Processing & AI';
  position: absolute;
  top: -0.75rem;
  left: 50%;
  transform: translateX(-50%);
  background: #0a0a0f;
  padding: 0 1rem;
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* Tech Grid */
.tech-details-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.tech-group-card {
  background: rgba(255, 255, 255, 0.015);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 20px;
  padding: 1.5rem;
  transition: transform 0.3s ease;
}

.tech-group-card:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.025);
  border-color: rgba(99, 102, 241, 0.2);
}

.group-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.group-icon {
  font-size: 1.5rem;
}

.group-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #f1f5f9;
}

.tech-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.tech-item {
  border-left: 2px solid rgba(255, 255, 255, 0.05);
  padding-left: 1rem;
}

.tech-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 0.25rem;
}

.tech-desc {
  font-size: 0.8125rem;
  color: #94a3b8;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .tech-stack-view {
    padding: 1rem;
  }
  
  .node-group {
    flex-direction: column;
    align-items: center;
  }
  
  .tech-details-section {
    grid-template-columns: 1fr;
  }
}
</style>

