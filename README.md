# Media Travel Data Analysis Platform

> 一个"**媒体数据爬取 → 旅行数据分析 → Neo4j 存储 → 前端可视化**"的完整系统
>
> 专注于：**旅行媒体数据洞察与趋势分析**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.x-green.svg)
![Vue.js](https://img.shields.io/badge/Vue.js-3-brightgreen.svg)
![Neo4j](https://img.shields.io/badge/Neo4j-5.x-008cc1.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

## 🎯 项目概述

本项目是一个专业的媒体旅行数据分析平台，专注于从各类媒体源抓取旅行相关数据，通过智能分析构建旅行知识图谱，并提供直观的Web界面进行交互式展示。系统能够洞察旅行趋势、分析热门目的地、挖掘旅游关联性，为旅行行业决策提供数据支持。

### 核心功能

- 🕷️ **多源媒体爬虫** - 支持新闻网站、旅游博客、社交媒体等多种数据源
- 🧳 **旅行数据挖掘** - 自动提取目的地、景点、酒店、交通等旅行相关信息
- 📊 **关系图谱构建** - 构建目的地关联、景点推荐、旅行路线知识图谱
- 📈 **趋势分析洞察** - 分析热门旅行趋势、季节性模式、用户偏好变化
- 🎨 **交互式可视化** - 基于ECharts/Cytoscape.js的动态旅行图谱展示
- ⚡ **异步任务处理** - 基于Celery的分布式数据处理队列
- 🤖 **智能内容分析** - 集成Coze AI进行内容理解和关系抽取
- 🐳 **容器化部署** - 完整的Docker Compose解决方案

## 🏗️ 技术架构

### 技术栈

| 层面 | 技术选型 |
|------|---------|
| **后端框架** | Django 5.x + Django Ninja API |
| **数据库** | PostgreSQL 15+ (关系数据) |
| **图数据库** | Neo4j 5.x (旅行图谱存储) |
| **任务队列** | Celery 5.x + Redis 7.x |
| **爬虫引擎** | httpx + BeautifulSoup4 + lxml |
| **AI分析** | Coze AI集成 (内容理解) |
| **前端框架** | Vue 3 + Vite + TypeScript |
| **可视化** | ECharts / Cytoscape.js |
| **容器化** | Docker + Docker Compose |
| **Web服务器** | Nginx + Gunicorn |

### 系统架构图

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue 3 前端    │    │   Django API    │    │   Celery Worker │
│                 │◄──►│                 │◄──►│                 │
│  - 媒体任务管理  │    │  - REST API     │    │  - 媒体爬虫     │
│  - 旅行图谱展示  │    │  - 数据验证     │    │  - 数据分析     │
│  - 趋势分析仪表盘│    │  - AI集成接口   │    │  - Neo4j同步    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │  PostgreSQL     │    │     Neo4j       │
│                 │    │                 │    │                 │
│  - 反向代理     │    │  - 媒体任务数据  │    │  - 旅行图谱     │
│  - 静态文件     │    │  - 爬取结果     │    │  - 目的地关系    │
│  - 负载均衡     │    │  - 分析报告     │    │  - 路线推荐     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                 │
                                 ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │                 │
                       │  - 消息队列     │
                       │  - 缓存存储     │
                       │  - 任务结果     │
                       └─────────────────┘
```

## 📁 项目结构

```
media-travel-analysis/
│
├── docker-compose.yml              # 容器编排配置
├── docker-compose.dev.yml          # 开发环境配置
├── .env.example                    # 环境变量模板
├── .gitignore
├── README.md                       # 项目说明文档
├── Makefile                        # 常用命令快捷方式
│
├── backend/                        # Django 后端
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── requirements/               # Python依赖管理
│   │   ├── base.txt
│   │   ├── dev.txt
│   │   └── prod.txt
│   ├── pyproject.toml
│   ├── manage.py
│   │
│   ├── config/                     # Django项目配置
│   │   ├── settings/               # 分环境配置
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   └── celery.py               # Celery配置
│   │
│   ├── apps/                       # Django应用模块
│   │   ├── crawl/                  # 媒体爬虫任务管理
│   │   │   ├── models.py           # 数据模型
│   │   │   ├── schemas.py          # API Schema
│   │   │   ├── api.py              # API路由
│   │   │   ├── tasks.py            # 异步任务
│   │   │   └── enums.py            # 枚举定义
│   │   │
│   │   ├── travel/                 # 旅行数据分析模块
│   │   │   ├── models.py           # 旅行数据模型
│   │   │   ├── schemas.py          # 旅行数据Schema
│   │   │   ├── api.py              # 旅行分析API
│   │   │   ├── analyzers.py        # 数据分析器
│   │   │   └── trends.py           # 趋势分析
│   │   │
│   │   ├── graph/                  # 旅行图谱查询模块
│   │   │   ├── api.py
│   │   │   ├── queries.py
│   │   │   ├── schemas.py
│   │   │   └── travel_graph.py     # 旅行图谱构建
│   │   │
│   │   └── ai/                     # AI分析模块
│   │       ├── coze_client.py      # Coze AI集成
│   │       ├── content_analyzer.py # 内容分析器
│   │       └── travel_extractor.py # 旅行信息抽取
│   │
│   ├── services/                   # 业务服务层
│   │   ├── neo4j_client.py         # Neo4j操作
│   │   ├── neo4j_sync.py           # 数据同步
│   │   ├── crawl_service.py        # 爬虫业务逻辑
│   │   ├── travel_analysis.py      # 旅行分析服务
│   │   └── ai_service.py           # AI分析服务
│   │
│   └── crawler/                    # 媒体爬虫引擎
│       ├── base.py                 # 爬虫基类
│       ├── media/                  # 媒体源爬虫
│       │   ├── news_crawler.py     # 新闻爬虫
│       │   ├── blog_crawler.py     # 博客爬虫
│       │   ├── social_crawler.py   # 社交媒体爬虫
│       │   └── travel_crawler.py   # 旅游网站爬虫
│       │
│       └── utils/                  # 爬虫工具
│           ├── http_client.py
│           ├── text_processor.py
│           ├── travel_extractor.py # 旅行信息提取
│           ├── retry.py
│           └── anti_crawl.py
│
├── frontend/                       # Vue3前端
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   │
│   └── src/
│       ├── views/                  # 页面视图
│       │   ├── HomeView.vue        # 首页仪表盘
│       │   ├── MediaTaskView.vue   # 媒体任务管理
│       │   ├── TaskDetailView.vue  # 任务详情
│       │   ├── TravelGraphView.vue # 旅行图谱可视化
│       │   └── TrendAnalysisView.vue # 趋势分析页
│       │
│       ├── components/             # 可复用组件
│       │   ├── layout/             # 布局组件
│       │   ├── common/             # 通用组件
│       │   ├── media/              # 媒体任务组件
│       │   ├── travel/             # 旅行分析组件
│       │   └── graph/              # 图谱相关组件
│       │
│       ├── api/                    # API请求封装
│       ├── stores/                 # Pinia状态管理
│       ├── composables/            # 组合式函数
│       ├── types/                  # TypeScript类型
│       └── utils/                  # 工具函数
│
├── nginx/                          # Nginx配置
│   ├── nginx.conf
│   └── conf.d/default.conf
│
└── scripts/                        # 辅助脚本
    ├── init_db.sh                  # 数据库初始化
    ├── init_neo4j.sh               # Neo4j初始化
    └── wait_for_it.sh              # 服务等待脚本
```

## 🚀 快速开始

### 环境要求

- Docker & Docker Compose
- Python 3.11+ (开发环境)
- Node.js 18+ (开发环境)
- Git

### 一键启动（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd media-travel-analysis

# 复制环境变量配置
cp .env.example .env

# 启动所有服务
docker-compose up -d

# 初始化数据库
docker-compose exec backend python manage.py migrate

# 创建超级用户（可选）
docker-compose exec backend python manage.py createsuperuser

# 访问应用
# 前端：http://localhost:3000
# 后端API：http://localhost:8000/api/v1
# Neo4j浏览器：http://localhost:7474
```

### 开发环境设置

#### 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements/dev.txt

# 环境变量配置
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等

# 数据库迁移
python manage.py migrate

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000

# 启动Celery Worker (新终端)
celery -A config.celery worker -l info

# 启动Celery Beat (可选，新终端)
celery -A config.celery beat -l info
```

#### 前端设置

```bash
cd frontend

# 安装依赖
npm install
# 或使用 pnpm
pnpm install

# 启动开发服务器
npm run dev
# 或
pnpm dev
```

## 📊 数据模型

### PostgreSQL 关系数据模型

#### MediaCrawlTask（媒体爬取任务）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| target_url | VARCHAR(500) | 目标URL |
| source_type | VARCHAR(50) | 媒体类型：news/blog/social/travel |
| crawl_type | VARCHAR(50) | 爬取类型：travel_content/article/list |
| status | VARCHAR(20) | PENDING/RUNNING/DONE/FAILED |
| total_items | INTEGER | 已爬取数量 |
| travel_relevant_count | INTEGER | 旅行相关内容数量 |
| created_at | TIMESTAMP | 创建时间 |
| started_at | TIMESTAMP | 开始时间 |
| finished_at | TIMESTAMP | 完成时间 |
| error_message | TEXT | 错误信息 |
| celery_task_id | VARCHAR(255) | Celery任务ID |

#### TravelContent（旅行内容）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| task | ForeignKey | 关联MediaCrawlTask |
| title | VARCHAR(300) | 标题 |
| url | VARCHAR(500) | URL |
| author | VARCHAR(100) | 作者/来源 |
| publish_time | TIMESTAMP | 发布时间 |
| content | TEXT | 内容 |
| summary | TEXT | AI生成摘要 |
| destinations | JSON | 提取的目的地 |
| attractions | JSON | 提取的景点 |
| hotels | JSON | 提取的酒店信息 |
| transportation | JSON | 交通信息 |
| travel_season | VARCHAR(50) | 旅行季节 |
| travel_type | VARCHAR(50) | 旅行类型 |
| sentiment_score | DECIMAL | 情感分析分数 |
| created_at | TIMESTAMP | 入库时间 |
| neo4j_synced | BOOLEAN | 是否已同步到Neo4j |

### Neo4j 旅行图数据模型

#### 节点类型

```cypher
// 媒体源节点
(:MediaSource {
  name: "媒体名称",
  domain: "example.com",
  type: "news/blog/social",
  created_at: datetime()
})

// 目的地节点
(:Destination {
  id: "destination_id",
  name: "目的地名称",
  country: "国家",
  region: "地区",
  type: "city/country/attraction",
  popularity_score: 8.5,
  created_at: datetime()
})

// 景点节点
(:Attraction {
  id: "attraction_id",
  name: "景点名称",
  destination: "所属目的地",
  category: "natural/historical/cultural",
  rating: 4.5,
  description: "景点描述"
})

// 内容节点
(:TravelContent {
  id: "uuid",
  title: "内容标题",
  url: "https://...",
  source: "来源媒体",
  publish_time: datetime(),
  sentiment_score: 0.8,
  travel_type: "leisure/business"
})

// 旅行者节点
(:Traveler {
  id: "traveler_id",
  name: "旅行者/博主",
  type: "influencer/regular/business",
  follower_count: 10000,
  preferred_destinations: ["巴黎", "东京"]
})

// 季节节点
(:Season {
  name: "春季/夏季/秋季/冬季",
  months: "3-5月",
  peak_season: true
})
```

#### 关系类型

```cypher
(:MediaSource)-[:PUBLISHES]->(:TravelContent)
(:TravelContent)-[:MENTIONS_DESTINATION]->(:Destination)
(:TravelContent)-[:FEATURES_ATTRACTION]->(:Attraction)
(:TravelContent)-[:WRITTEN_BY]->(:Traveler)
(:Destination)-[:CONTAINS]->(:Attraction)
(:Destination)-[:BEST_SEASON]->(:Season)
(:Destination)-[:RELATED_TO {strength: 0.8}]->(:Destination)
(:Attraction)-[:NEAR]->(:Attraction)
(:Traveler)-[:PREFERS]->(:Destination)
(:TravelContent)-[:HAS_SENTIMENT {score: 0.9}]->(:Destination)
```

## 🔌 API 文档

### 媒体爬虫任务 API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/crawl/media/tasks` | 创建媒体爬取任务 |
| GET | `/api/v1/crawl/media/tasks` | 获取媒体任务列表 |
| GET | `/api/v1/crawl/media/tasks/{id}` | 获取任务详情 |
| DELETE | `/api/v1/crawl/media/tasks/{id}` | 取消/删除任务 |
| GET | `/api/v1/crawl/media/tasks/{id}/content` | 获取爬取的旅行内容 |

### 旅行数据分析 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/travel/analysis/destinations` | 获取热门目的地排行 |
| GET | `/api/v1/travel/analysis/trends` | 获取旅行趋势分析 |
| GET | `/api/v1/travel/analysis/seasonality` | 获取季节性分析 |
| GET | `/api/v1/travel/analysis/sentiment` | 获取情感分析报告 |
| GET | `/api/v1/travel/analysis/recommendations` | 获取旅行推荐 |

### 旅行图谱 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/graph/travel/destinations` | 获取目的地关系图谱 |
| GET | `/api/v1/graph/travel/routes` | 获取推荐路线图谱 |
| GET | `/api/v1/graph/travel/node/{node_id}` | 获取节点详情 |
| GET | `/api/v1/graph/travel/search` | 搜索旅行节点 |
| GET | `/api/v1/graph/travel/influences` | 获取媒体影响力分析 |

### AI分析 API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/ai/analyze/content` | 分析内容旅行相关信息 |
| POST | `/api/v1/ai/extract/entities` | 提取旅行实体信息 |
| POST | `/api/v1/ai/sentiment/analysis` | 情感分析 |
| GET | `/api/v1/ai/summary/destination/{id}` | 获取目的地AI摘要 |

#### 请求示例

**创建媒体爬取任务**

```bash
curl -X POST http://localhost:8000/api/v1/crawl/media/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "target_url": "https://travel.blog.example.com",
    "source_type": "blog",
    "crawl_type": "travel_content",
    "depth": 2,
    "max_pages": 100
  }'
```

**获取旅行趋势分析**

```bash
curl "http://localhost:8000/api/v1/travel/analysis/trends?period=6m&region=asia"
```

**获取目的地关系图谱**

```bash
curl "http://localhost:8000/api/v1/graph/travel/destinations?destination=日本&depth=2"
```

**响应示例**

```json
{
  "nodes": [
    {
      "id": "dest_1",
      "label": "Destination",
      "properties": {
        "name": "东京",
        "country": "日本",
        "popularity_score": 9.2,
        "category": "city"
      }
    },
    {
      "id": "attr_1",
      "label": "Attraction",
      "properties": {
        "name": "浅草寺",
        "category": "cultural",
        "rating": 4.5
      }
    }
  ],
  "edges": [
    {
      "source": "dest_1",
      "target": "attr_1",
      "type": "CONTAINS",
      "properties": {
        "distance": "2.5km",
        "visit_duration": "2-3 hours"
      }
    }
  ],
  "analytics": {
    "total_destinations": 45,
    "total_attractions": 230,
    "average_sentiment": 0.78,
    "trending_destinations": ["东京", "大阪", "京都"]
  }
}
```

## 🎨 前端功能

### 页面路由

| 路由 | 页面 | 功能说明 |
|------|------|----------|
| `/` | 首页仪表盘 | 旅行数据概览、热门目的地、趋势图表 |
| `/media-tasks` | 媒体任务管理 | 创建爬虫任务、任务列表、进度监控 |
| `/tasks/:id` | 任务详情 | 查看爬取结果、内容分析、数据质量评估 |
| `/travel-graph` | 旅行图谱可视化 | 交互式目的地关系图谱、路线规划 |
| `/trends` | 趋势分析 | 旅行趋势洞察、季节性分析、情感变化 |

### 核心功能特性

#### 媒体任务管理系统
- ✅ 多源URL输入（新闻、博客、社交媒体、旅游网站）
- ✅ 媒体类型识别和分类
- ✅ 旅行相关内容智能筛选
- ✅ 实时任务状态和进度显示
- ✅ 数据质量评估指标
- ✅ 任务调度和批量管理

#### 旅行数据分析
- ✅ 热门目的地排行榜
- ✅ 旅行趋势时间线分析
- ✅ 季节性模式识别
- ✅ 情感分析和用户偏好洞察
- ✅ 旅行类型分布统计
- ✅ 媒体影响力分析

#### 旅行图谱可视化
- ✅ 基于ECharts/Cytoscape.js的交互式地图
- ✅ 目的地关系网络展示
- ✅ 景点推荐和路线规划
- ✅ 季节性最佳旅行时间提示
- ✅ 用户评价和情感可视化
- ✅ 多层级数据钻取

#### AI智能分析
- ✅ 自动内容理解和实体抽取
- ✅ 旅行相关性智能判断
- ✅ 个性化推荐算法
- ✅ 情感分析和观点挖掘
- ✅ 趋势预测和异常检测

## 🔧 配置说明

### 环境变量配置

创建 `.env` 文件并配置以下变量：

```bash
# Django配置
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL配置
POSTGRES_DB=media_travel_analysis
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Neo4j配置
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Redis配置
REDIS_URL=redis://redis:6379/0

# Celery配置
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

# 媒体爬虫配置
CRAWL_REQUEST_DELAY=1.0
CRAWL_MAX_RETRIES=3
CRAWL_TIMEOUT=30
CRAWL_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

# AI分析配置
COZE_API_KEY=your-coze-api-key
COZE_API_URL=https://api.coze.com/v1
COZE_MODEL=travel-analysis-v1

# 旅行数据配置
TRAVEL_KEYWORDS_FILE=config/travel_keywords.txt
DESTINATION_DATABASE_FILE=config/destinations.json
MIN_TRAVEL_RELEVANCE_SCORE=0.7
```

### 媒体爬虫配置

#### 支持的媒体源类型

- **新闻网站**: 各大新闻媒体的旅游版块
- **旅游博客**: 专业旅行博主内容
- **社交媒体**: 微博、小红书等平台旅行内容
- **旅游网站**: 马蜂窝、携程等攻略内容

#### 旅行内容识别规则

```python
# 在 crawler/utils/travel_extractor.py 中配置
TRAVEL_KEYWORDS = [
    # 目的地类型
    '景点', '景区', '博物馆', '公园', '海滩', '山脉',
    # 旅行行为
    '旅游', '旅行', '度假', '出游', '观光', '探索',
    # 交通住宿
    '酒店', '民宿', '航班', '火车', '地铁', '租车',
    # 旅行体验
    '美食', '购物', '文化', '历史', '自然', '冒险'
]

DESTINATION_PATTERNS = [
    r'([一-龥]{2,4}(市|县|镇|村))',
    r'([一-龥]{2,4}(省|州|国))',
    r'(\d{1,2}天\d{1,2}夜)',
    r'(自由行|跟团游|定制游)'
]
```

#### 内容质量评估

```python
# 旅行内容质量评分标准
QUALITY_FACTORS = {
    'content_length': {'min': 500, 'weight': 0.2},
    'travel_info_count': {'min': 3, 'weight': 0.3},
    'image_count': {'min': 2, 'weight': 0.2},
    'structured_data': {'has_hours_price': True, 'weight': 0.3}
}
```

## 🛠️ 开发指南

### 添加新媒体源爬虫

1. 在 `crawler/media/` 目录下创建新的爬虫模块
2. 继承 `BaseMediaCrawler` 类
3. 实现 `extract_travel_info()` 方法
4. 在 `tasks.py` 中注册新爬虫

```python
# crawler/media/travel_blog_crawler.py
from ..base import BaseMediaCrawler

class TravelBlogCrawler(BaseMediaCrawler):
    def extract_travel_info(self, response):
        # 实现旅行信息提取逻辑
        destinations = self.extract_destinations(response.text)
        attractions = self.extract_attractions(response.text)
        hotels = self.extract_hotels(response.text)

        return {
            'destinations': destinations,
            'attractions': attractions,
            'hotels': hotels,
            'travel_type': self.classify_travel_type(response.text)
        }
```

### 扩展旅行图谱节点

1. 在 `services/travel_graph.py` 中添加新节点类型
2. 更新 `graph/queries.py` 中的Cypher查询
3. 在前端添加相应的可视化样式

```python
# 新增餐厅节点示例
class RestaurantNode:
    def __init__(self, name, cuisine, rating, price_range):
        self.name = name
        self.cuisine = cuisine
        self.rating = rating
        self.price_range = price_range

    def to_neo4j(self):
        return {
            'name': self.name,
            'cuisine': self.cuisine,
            'rating': self.rating,
            'price_range': self.price_range
        }
```

### 自定义AI分析模型

1. 在 `apps/ai/` 目录下创建新的分析器
2. 实现 `ContentAnalyzer` 接口
3. 注册到AI服务中

```python
# apps/ai/custom_analyzer.py
from .content_analyzer import ContentAnalyzer

class CustomTravelAnalyzer(ContentAnalyzer):
    def analyze(self, content):
        # 自定义分析逻辑
        entities = self.extract_entities(content)
        sentiment = self.analyze_sentiment(content)
        travel_theme = self.classify_travel_theme(content)

        return AnalysisResult(
            entities=entities,
            sentiment=sentiment,
            travel_theme=travel_theme
        )
```

## 🧪 测试

### 运行测试

```bash
# 后端测试
cd backend
python manage.py test

# 前端测试
cd frontend
npm run test
```

### 测试覆盖率

```bash
# 后端覆盖率
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📦 部署指南

### 生产环境部署

1. **环境准备**
   ```bash
   # 生产环境配置
   cp .env.example .env.production
   # 编辑生产环境变量
   ```

2. **构建镜像**
   ```bash
   docker-compose -f docker-compose.yml build
   ```

3. **启动服务**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

4. **初始化数据**
   ```bash
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py collectstatic --noinput
   ```

### 性能优化

- **数据库优化**
  - PostgreSQL索引优化
  - Neo4j查询优化

- **缓存策略**
  - Redis缓存热点数据
  - 静态文件CDN

- **爬虫优化**
  - 并发控制
  - 请求池管理
  - 反爬策略

- **AI分析优化**
  - 批量处理模式
  - 模型响应缓存
  - 异步分析队列

## 📝 更新日志

### v2.0.0 (2024-12-21)
- ✅ 转型为媒体旅行数据分析平台
- ✅ 集成Coze AI智能分析
- ✅ 新增旅行内容智能提取
- ✅ 实现旅行图谱可视化
- ✅ 添加旅行趋势分析功能

### v1.5.0 (2024-12-01)
- ✅ 完成媒体数据爬取架构
- ✅ 实现多源媒体支持
- ✅ 添加内容质量评估
- ✅ 集成Neo4j图谱存储

### v1.0.0 (2024-01-20)
- ✅ 完成基础架构设计
- ✅ 实现基础爬虫功能
- ✅ 搭建Docker开发环境
- ✅ 开发Vue3前端界面

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- Python: 遵循 PEP 8
- JavaScript/TypeScript: 使用 ESLint + Prettier
- Git提交信息: 使用约定式提交格式

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目链接: [https://github.com/yourusername/media-travel-analysis](https://github.com/yourusername/media-travel-analysis)
- 问题反馈: [Issues](https://github.com/yourusername/media-travel-analysis/issues)
- 邮箱: your.email@example.com

## 🙏 致谢

- [Django](https://www.djangoproject.com/) - Web框架
- [Vue.js](https://vuejs.org/) - 前端框架
- [Neo4j](https://neo4j.com/) - 图数据库
- [Celery](https://docs.celeryproject.org/) - 异步任务队列
- [ECharts](https://echarts.apache.org/) - 数据可视化
- [Coze AI](https://coze.com/) - AI分析服务

## 🌟 旅行行业应用

本项目特别适用于以下旅行行业场景：

### 旅游企业决策支持
- 📊 **市场趋势分析** - 洞察热门目的地和旅行偏好变化
- 🎯 **竞品分析** - 监控竞争对手的媒体表现和用户反馈
- 📈 **营销策略优化** - 基于数据驱动的营销决策

### 内容创作者工具
- ✍️ **内容灵感发现** - 发现热门旅行话题和创作方向
- 🗺️ **目的地深度挖掘** - 获取目的地的详细信息和关联推荐
- 📱 **社交媒体优化** - 提升内容在社交平台的传播效果

### 旅游研究机构
- 🔬 **旅行行为研究** - 分析用户旅行模式和偏好
- 🌍 **目的地影响力评估** - 评估各目的地的媒体曝光和情感倾向
- 📋 **政策制定支持** - 为旅游政策制定提供数据依据

---

⭐ 如果这个项目对您的旅行业务有帮助，请给它一个星标！