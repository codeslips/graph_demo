# 澎湃新闻 Web Crawl → Graph Insight Demo

> 一个"**可配置爬取 → 后台异步执行 → Neo4j 存储 → 前端可视化**"的完整系统
> 数据源：**澎湃新闻 (ThePaper)**

---

## 核心目标

1. 从澎湃新闻抓取数据
2. 以「关系」方式存到 Neo4j
3. 在前端可视化展示

---

# 一、技术栈

| 层          | 技术                             |
| ----------- | -------------------------------- |
| Backend     | Django 5.x + Django Ninja        |
| DB          | PostgreSQL 15+                   |
| Graph DB    | Neo4j 5.x                        |
| Task Queue  | Celery 5.x + Redis 7.x           |
| Crawler     | httpx + BeautifulSoup4 + lxml    |
| Frontend    | Vue 3 + Vite + TypeScript        |
| Graph Viz   | ECharts / Cytoscape.js           |
| Container   | Docker + Docker Compose          |

---

# 二、完整项目目录结构

```text
thepaper-graph/
│
├── docker-compose.yml              # 容器编排配置
├── docker-compose.dev.yml          # 开发环境 compose
├── .env.example                    # 环境变量模板
├── .gitignore
├── README.md
├── Makefile                        # 常用命令快捷方式
│
├── backend/                        # Django 后端
│   ├── Dockerfile
│   ├── Dockerfile.dev              # 开发用 Dockerfile
│   ├── requirements/
│   │   ├── base.txt                # 基础依赖
│   │   ├── dev.txt                 # 开发依赖
│   │   └── prod.txt                # 生产依赖
│   ├── pyproject.toml              # 项目元信息
│   ├── manage.py
│   │
│   ├── config/                     # Django 项目配置
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # 基础配置
│   │   │   ├── development.py      # 开发环境配置
│   │   │   └── production.py       # 生产环境配置
│   │   ├── urls.py                 # 主路由
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   └── celery.py               # Celery 配置
│   │
│   ├── apps/                       # Django 应用
│   │   ├── __init__.py
│   │   │
│   │   ├── crawl/                  # 爬虫任务模块
│   │   │   ├── __init__.py
│   │   │   ├── admin.py            # Admin 后台配置
│   │   │   ├── apps.py
│   │   │   ├── models.py           # CrawlTask, CrawlItem 模型
│   │   │   ├── schemas.py          # Django Ninja 请求/响应 schemas
│   │   │   ├── api.py              # Django Ninja API 路由
│   │   │   ├── tasks.py            # Celery 异步任务
│   │   │   ├── enums.py            # 状态枚举定义
│   │   │   ├── migrations/
│   │   │   │   └── __init__.py
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       ├── test_models.py
│   │   │       ├── test_api.py
│   │   │       └── test_tasks.py
│   │   │
│   │   └── graph/                  # 图谱查询模块
│   │       ├── __init__.py
│   │       ├── apps.py
│   │       ├── schemas.py          # 图数据响应 schemas
│   │       ├── api.py              # 图谱 API 路由
│   │       ├── queries.py          # Cypher 查询语句
│   │       └── tests/
│   │           ├── __init__.py
│   │           └── test_api.py
│   │
│   ├── core/                       # 核心通用模块
│   │   ├── __init__.py
│   │   ├── exceptions.py           # 自定义异常
│   │   ├── pagination.py           # 分页配置
│   │   └── middleware.py           # 中间件
│   │
│   ├── services/                   # 业务服务层
│   │   ├── __init__.py
│   │   ├── neo4j_client.py         # Neo4j 连接与操作
│   │   ├── neo4j_sync.py           # 数据同步到 Neo4j
│   │   └── crawl_service.py        # 爬虫业务逻辑编排
│   │
│   └── crawler/                    # 爬虫模块
│       ├── __init__.py
│       ├── base.py                 # 爬虫基类
│       ├── thepaper/               # 澎湃新闻专用爬虫
│       │   ├── __init__.py
│       │   ├── news_list.py        # 新闻列表爬虫
│       │   ├── article.py          # 文章详情爬虫
│       │   ├── channel.py          # 频道爬虫
│       │   ├── parser.py           # 页面解析器
│       │   ├── selectors.py        # CSS/XPath 选择器配置
│       │   └── config.py           # 爬虫配置（URL、请求头等）
│       └── utils/
│           ├── __init__.py
│           ├── http_client.py      # HTTP 请求封装（httpx）
│           ├── text_processor.py   # 文本处理（分词、关键词提取）
│           ├── retry.py            # 重试装饰器
│           └── anti_crawl.py       # 反爬虫处理
│
├── frontend/                       # Vue3 前端
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── env.d.ts
│   ├── index.html
│   ├── .eslintrc.cjs
│   ├── .prettierrc.json
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   └── logo.svg
│   │
│   └── src/
│       ├── main.ts                 # 入口文件
│       ├── App.vue                 # 根组件
│       │
│       ├── api/                    # API 请求封装
│       │   ├── index.ts            # API 统一导出
│       │   ├── request.ts          # axios 实例配置
│       │   ├── crawl.ts            # 爬虫任务 API
│       │   └── graph.ts            # 图谱数据 API
│       │
│       ├── router/                 # 路由配置
│       │   └── index.ts
│       │
│       ├── stores/                 # Pinia 状态管理
│       │   ├── index.ts
│       │   ├── task.ts             # 任务状态
│       │   └── graph.ts            # 图谱状态
│       │
│       ├── views/                  # 页面视图
│       │   ├── HomeView.vue        # 首页/仪表盘
│       │   ├── TaskListView.vue    # 任务管理页
│       │   ├── TaskDetailView.vue  # 任务详情页
│       │   └── GraphView.vue       # 关系图谱页
│       │
│       ├── components/             # 组件
│       │   ├── layout/             # 布局组件
│       │   │   ├── AppHeader.vue
│       │   │   ├── AppSidebar.vue
│       │   │   └── AppLayout.vue
│       │   │
│       │   ├── common/             # 通用组件
│       │   │   ├── StatusBadge.vue     # 状态徽章
│       │   │   ├── LoadingSpinner.vue  # 加载动画
│       │   │   ├── ConfirmDialog.vue   # 确认弹窗
│       │   │   └── EmptyState.vue      # 空状态
│       │   │
│       │   ├── task/               # 任务相关组件
│       │   │   ├── TaskForm.vue        # 创建任务表单
│       │   │   ├── TaskCard.vue        # 任务卡片
│       │   │   ├── TaskTable.vue       # 任务列表表格
│       │   │   ├── TaskProgress.vue    # 任务进度条
│       │   │   └── TaskItemList.vue    # 爬取结果列表
│       │   │
│       │   └── graph/              # 图谱相关组件
│       │       ├── GraphCanvas.vue     # 图谱画布（ECharts/Cytoscape）
│       │       ├── NodeDetail.vue      # 节点详情面板
│       │       ├── GraphToolbar.vue    # 图谱工具栏
│       │       ├── GraphLegend.vue     # 图例
│       │       └── GraphSearch.vue     # 图谱搜索
│       │
│       ├── composables/            # 组合式函数
│       │   ├── useTask.ts          # 任务相关逻辑
│       │   ├── useGraph.ts         # 图谱相关逻辑
│       │   └── usePolling.ts       # 轮询状态更新
│       │
│       ├── types/                  # TypeScript 类型定义
│       │   ├── index.ts
│       │   ├── crawl.ts            # 爬虫相关类型
│       │   └── graph.ts            # 图谱相关类型
│       │
│       ├── utils/                  # 工具函数
│       │   ├── format.ts           # 格式化函数
│       │   ├── date.ts             # 日期处理
│       │   └── constants.ts        # 常量定义
│       │
│       └── styles/                 # 样式
│           ├── main.css            # 主样式
│           ├── variables.css       # CSS 变量
│           └── transitions.css     # 过渡动画
│
├── nginx/                          # Nginx 配置
│   ├── Dockerfile
│   ├── nginx.conf                  # 主配置
│   └── conf.d/
│       └── default.conf            # 站点配置
│
└── scripts/                        # 辅助脚本
    ├── init_db.sh                  # 数据库初始化
    ├── init_neo4j.sh               # Neo4j 初始化
    ├── wait_for_it.sh              # 服务等待脚本
    └── entrypoint.sh               # 容器入口脚本
```

---

# 三、PostgreSQL 数据模型

## CrawlTask（爬取任务）

| 字段           | 类型         | 说明                                          |
| -------------- | ------------ | --------------------------------------------- |
| id             | UUID         | 主键                                          |
| target_url     | VARCHAR(500) | 目标 URL                                      |
| crawl_type     | VARCHAR(50)  | 爬取类型：`news_list` / `article` / `channel` |
| status         | VARCHAR(20)  | `PENDING` / `RUNNING` / `DONE` / `FAILED`     |
| total_items    | INTEGER      | 已爬取数量                                    |
| created_at     | TIMESTAMP    | 创建时间                                      |
| started_at     | TIMESTAMP    | 开始时间                                      |
| finished_at    | TIMESTAMP    | 完成时间                                      |
| error_message  | TEXT         | 错误信息                                      |
| celery_task_id | VARCHAR(255) | Celery 任务 ID                                |

## CrawlItem（爬取结果索引）

| 字段         | 类型         | 说明               |
| ------------ | ------------ | ------------------ |
| id           | UUID         | 主键               |
| task         | ForeignKey   | 关联 CrawlTask     |
| title        | VARCHAR(300) | 文章标题           |
| url          | VARCHAR(500) | 文章 URL           |
| author       | VARCHAR(100) | 作者/来源          |
| publish_time | TIMESTAMP    | 发布时间           |
| summary      | TEXT         | 摘要               |
| category     | VARCHAR(100) | 分类/频道          |
| created_at   | TIMESTAMP    | 入库时间           |
| neo4j_synced | BOOLEAN      | 是否已同步到 Neo4j |

---

# 四、Neo4j 图模型

## 节点类型（Labels）

```cypher
(:Website {
  name: "澎湃新闻",
  domain: "thepaper.cn",
  created_at: datetime()
})

(:Channel {
  id: "channel_id",
  name: "时事",
  url: "https://...",
  description: "..."
})

(:Article {
  id: "uuid",
  title: "新闻标题",
  url: "https://...",
  author: "作者",
  publish_time: datetime(),
  summary: "摘要..."
})

(:Keyword {
  name: "关键词",
  frequency: 10
})

(:Author {
  name: "作者名"
})
```

## 关系类型（Relationships）

```cypher
(:Website)-[:HAS_CHANNEL]->(:Channel)
(:Channel)-[:CONTAINS]->(:Article)
(:Article)-[:MENTIONS {weight: 3}]->(:Keyword)
(:Article)-[:WRITTEN_BY]->(:Author)
(:Article)-[:LINKS_TO]->(:Article)
(:Keyword)-[:RELATED_TO {strength: 0.8}]->(:Keyword)
```

## 示例 Cypher 查询

```cypher
// 获取某任务的完整图谱数据
MATCH (w:Website)-[:HAS_CHANNEL]->(c:Channel)-[:CONTAINS]->(a:Article)
WHERE a.task_id = $task_id
OPTIONAL MATCH (a)-[m:MENTIONS]->(k:Keyword)
RETURN w, c, a, m, k

// 获取热门关键词
MATCH (k:Keyword)<-[m:MENTIONS]-(a:Article)
RETURN k.name, COUNT(m) as frequency
ORDER BY frequency DESC
LIMIT 20
```

---

# 五、Celery 异步任务流程

```text
start_crawl_task(task_id)
 │
 ├─► 更新状态 → RUNNING
 │
 ├─► 执行爬虫
 │    ├── 获取页面列表
 │    ├── 遍历解析每篇文章
 │    ├── 提取关键词
 │    └── 构建关系数据
 │
 ├─► 写入 PostgreSQL
 │    └── 批量创建 CrawlItem
 │
 ├─► 写入 Neo4j
 │    ├── 创建/更新节点
 │    └── 创建关系
 │
 ├─► 更新状态 → DONE
 │
 └─► 异常处理 → FAILED + error_message
```

---

# 六、Django Ninja API 设计

## 爬虫任务 API

| Method | Endpoint                       | 说明         |
| ------ | ------------------------------ | ------------ |
| POST   | `/api/v1/crawl/tasks`          | 创建爬取任务 |
| GET    | `/api/v1/crawl/tasks`          | 获取任务列表 |
| GET    | `/api/v1/crawl/tasks/{id}`     | 获取任务详情 |
| DELETE | `/api/v1/crawl/tasks/{id}`     | 取消/删除任务|
| GET    | `/api/v1/crawl/tasks/{id}/items` | 获取爬取结果 |

## 图谱 API

| Method | Endpoint                       | 说明           |
| ------ | ------------------------------ | -------------- |
| GET    | `/api/v1/graph/task/{id}`      | 获取任务图谱数据 |
| GET    | `/api/v1/graph/keywords`       | 获取热门关键词 |
| GET    | `/api/v1/graph/node/{node_id}` | 获取节点详情   |
| GET    | `/api/v1/graph/search`         | 搜索节点       |

## 请求/响应示例

### 创建任务

```http
POST /api/v1/crawl/tasks
Content-Type: application/json

{
  "target_url": "https://www.thepaper.cn/channel_xxxxx",
  "crawl_type": "news_list"
}
```

### 获取图谱数据

```http
GET /api/v1/graph/task/{id}
```

```json
{
  "nodes": [
    {"id": "n1", "label": "Article", "properties": {"title": "..."}},
    {"id": "n2", "label": "Keyword", "properties": {"name": "AI"}}
  ],
  "edges": [
    {"source": "n1", "target": "n2", "type": "MENTIONS", "weight": 3}
  ],
  "stats": {
    "total_nodes": 150,
    "total_edges": 420
  }
}
```

---

# 七、前端页面设计

## 页面路由

| 路由         | 页面       | 说明                   |
| ------------ | ---------- | ---------------------- |
| `/`          | 首页       | 数据概览仪表盘         |
| `/tasks`     | 任务管理   | 任务列表、创建新任务   |
| `/tasks/:id` | 任务详情   | 查看单个任务的详细信息 |
| `/graph/:id` | 图谱可视化 | 交互式关系图谱展示     |

## 核心功能

### 任务管理页

- ✅ URL 输入（支持澎湃新闻各频道）
- ✅ 爬取类型选择（新闻列表 / 单篇文章 / 频道全爬）
- ✅ 启动爬取按钮
- ✅ 任务列表（实时状态刷新）
- ✅ 任务进度条

### 图谱可视化页

- ✅ ECharts / Cytoscape 力导向图
- ✅ 节点拖拽、缩放
- ✅ 点击节点显示详情
- ✅ 节点类型筛选
- ✅ 关键词搜索定位
- ✅ 导出图片

---

# 八、Docker Compose 服务编排

```yaml
services:
  backend:      # Django + Gunicorn
  celery:       # Celery Worker
  celery-beat:  # Celery Beat (可选定时任务)
  redis:        # Redis (消息队列)
  postgres:     # PostgreSQL
  neo4j:        # Neo4j
  frontend:     # Vue3 Dev Server / Nginx
```

---

# 九、环境变量配置

```bash
# .env.example

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
POSTGRES_DB=thepaper_graph
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Neo4j
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

# 爬虫配置
CRAWL_REQUEST_DELAY=1.0
CRAWL_MAX_RETRIES=3
CRAWL_TIMEOUT=30
CRAWL_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
```

---

# 十、待补充（等你提供）

- [ ] 澎湃新闻具体 URL 结构
- [ ] 目标爬取频道/栏目
- [ ] 页面选择器（CSS / XPath）
- [ ] 是否需要登录/Cookie
- [ ] 爬取深度/数量限制
- [ ] 特殊反爬处理需求

---

# 十一、开发顺序建议

1. **Phase 1**: 项目初始化 + Docker 环境搭建
2. **Phase 2**: Django + Celery + Redis 基础配置
3. **Phase 3**: PostgreSQL 模型 + Neo4j 连接
4. **Phase 4**: 澎湃新闻爬虫核心逻辑
5. **Phase 5**: Django Ninja API 实现
6. **Phase 6**: Vue3 前端 + 图谱可视化

---

👉 **下一步**：请告诉我澎湃新闻的 URL 和你想要的爬取方式，我就开始写代码！
