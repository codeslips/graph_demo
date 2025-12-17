<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="home-view">
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="gradient-text">澎湃图谱</span>
        </h1>
        <p class="hero-subtitle">
          通过交互式知识图谱探索新闻关系。
          自动抓取澎湃新闻文章，并可视化频道、文章和标签之间的连接。
        </p>
        <div class="hero-actions">
          <RouterLink to="/tasks" class="btn btn-primary">
            开始使用 →
          </RouterLink>
        </div>
      </div>

      <div class="hero-visual">
        <div class="graph-preview">
          <div class="node node-channel">频道</div>
          <div class="edge edge-1"></div>
          <div class="node node-article">文章</div>
          <div class="edge edge-2"></div>
          <div class="node node-tag">标签</div>
        </div>
      </div>
    </section>

    <section class="features">
      <div class="feature-card">
        <div class="feature-icon">🕷️</div>
        <h3>智能爬取</h3>
        <p>基于 Celery 的异步爬虫引擎。自动提取文章、作者和标签。</p>
      </div>

      <div class="feature-card">
        <div class="feature-icon">🔗</div>
        <h3>图谱存储</h3>
        <p>Neo4j 图数据库存储文章、频道和关键词之间的关系。</p>
      </div>

      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>交互式可视化</h3>
        <p>使用力导向图探索知识图谱。点击节点查看详情。</p>
      </div>
    </section>

    <section class="tech-stack">
      <h2>Built With</h2>
      <div class="tech-grid">
        <div class="tech-item">Django + Ninja</div>
        <div class="tech-item">Vue 3 + TypeScript</div>
        <div class="tech-item">Neo4j</div>
        <div class="tech-item">Celery + Redis</div>
        <div class="tech-item">ECharts</div>
        <div class="tech-item">PostgreSQL</div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-view {
  min-height: calc(100vh - 60px);
  padding: 0;
}

/* Hero Section */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  padding: 4rem 2rem;
  min-height: 500px;
  align-items: center;
  background: radial-gradient(ellipse at 30% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 50%);
}

.hero-content {
  max-width: 560px;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.gradient-text {
  background: linear-gradient(135deg, #e0e0e0 0%, #8b5cf6 50%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: #8a8a9a;
  line-height: 1.7;
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.875rem 1.75rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(99, 102, 241, 0.4);
}

/* Graph Preview */
.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.graph-preview {
  position: relative;
  width: 300px;
  height: 300px;
}

.node {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 0.85rem;
  font-weight: 600;
  animation: float 3s ease-in-out infinite;
}

.node-channel {
  top: 50%;
  left: 10%;
  transform: translate(-50%, -50%);
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
  color: #1e1e2e;
  animation-delay: 0s;
}

.node-article {
  top: 20%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  animation-delay: 0.5s;
}

.node-tag {
  top: 75%;
  left: 75%;
  transform: translate(-50%, -50%);
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: #1e1e2e;
  animation-delay: 1s;
}

.edge {
  position: absolute;
  background: linear-gradient(90deg, rgba(99, 102, 241, 0.5) 0%, rgba(139, 92, 246, 0.5) 100%);
  height: 2px;
  transform-origin: left center;
}

.edge-1 {
  top: 35%;
  left: 25%;
  width: 80px;
  transform: rotate(-25deg);
}

.edge-2 {
  top: 50%;
  left: 55%;
  width: 80px;
  transform: rotate(45deg);
}

@keyframes float {
  0%, 100% { transform: translate(-50%, -50%) translateY(0); }
  50% { transform: translate(-50%, -50%) translateY(-10px); }
}

/* Features */
.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  padding: 4rem 2rem;
  background: linear-gradient(180deg, #0a0a12 0%, #12121a 100%);
}

.feature-card {
  background: linear-gradient(135deg, #1e1e2e 0%, #252538 100%);
  border: 1px solid #3d3d5c;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  transition: transform 0.2s, border-color 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
  border-color: #6366f1;
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.1rem;
  color: #e0e0e0;
  margin-bottom: 0.75rem;
}

.feature-card p {
  font-size: 0.9rem;
  color: #8a8a9a;
  line-height: 1.6;
}

/* Tech Stack */
.tech-stack {
  padding: 4rem 2rem;
  text-align: center;
}

.tech-stack h2 {
  font-size: 1.5rem;
  color: #a0a0b0;
  margin-bottom: 2rem;
}

.tech-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.tech-item {
  padding: 0.625rem 1.25rem;
  background: #1e1e2e;
  border: 1px solid #3d3d5c;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #a0a0b0;
}

/* Responsive */
@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-content {
    margin: 0 auto;
  }

  .hero-visual {
    display: none;
  }

  .features {
    grid-template-columns: 1fr;
  }
}
</style>
