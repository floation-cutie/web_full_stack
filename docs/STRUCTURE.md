# GoodServices 项目目录结构指南

本文档说明 GoodServices 项目的目录组织方式，帮助开发者快速定位和理解项目文件。

## 顶级目录结构

```
web_full_stack/
├── backend/                # FastAPI 后端应用
├── frontend/               # Vue 3 前端应用
├── database/               # 数据库相关文件
├── docs/                   # 项目文档
├── config/                 # 配置文件
├── specs/                  # 规范和设计文档
├── reports/                # 项目报告
├── test-artifacts/         # 测试工件
├── .gitignore              # Git 忽略配置
├── .env                    # 环境变量（不提交）
├── .env.example            # 环境变量示例
├── CLAUDE.md               # Claude AI 工作指南
├── README.md               # 项目说明（本文档）
└── STRUCTURE.md            # 目录结构指南（本文档）
```

## 详细目录说明

### backend/ - FastAPI 后端

后端应用实现所有业务逻辑，包括 API 端点、数据库操作和身份验证。

```
backend/
├── app/                    # 主应用模块
│   ├── main.py            # FastAPI 应用入口
│   ├── database.py         # 数据库连接配置
│   ├── dependencies.py     # 依赖注入（认证等）
│   │
│   ├── api/                # API 路由模块
│   │   └── v1/             # V1 API 版本
│   │       ├── auth.py     # 认证端点（login, register）
│   │       ├── users.py    # 用户管理端点
│   │       ├── service_requests.py  # 服务请求端点
│   │       ├── service_responses.py # 服务响应端点
│   │       ├── match.py    # 匹配接受端点
│   │       └── stats.py    # 统计分析端点
│   │
│   ├── models/             # SQLAlchemy ORM 模型
│   │   ├── user.py         # 用户模型
│   │   ├── service_request.py      # 服务请求模型
│   │   ├── service_response.py     # 服务响应模型
│   │   ├── accept_info.py  # 服务接受模型
│   │   ├── service_type.py # 服务类型模型
│   │   └── city_info.py    # 城市信息模型
│   │
│   ├── schemas/            # Pydantic 数据验证模型
│   │   ├── common.py       # 通用模式
│   │   ├── auth.py         # 认证请求响应模型
│   │   ├── user.py         # 用户 CRUD 模型
│   │   ├── service_request.py      # 服务请求模型
│   │   └── service_response.py     # 服务响应模型
│   │
│   ├── crud/               # 数据库 CRUD 操作
│   │   ├── user.py         # 用户 CRUD
│   │   ├── service_request.py      # 服务请求 CRUD
│   │   ├── service_response.py     # 服务响应 CRUD
│   │   ├── accept_info.py  # 接受信息 CRUD
│   │   └── stats.py        # 统计数据 CRUD
│   │
│   ├── core/               # 核心功能
│   │   ├── config.py       # 配置管理
│   │   ├── security.py     # JWT、密码哈希等
│   │   └── exceptions.py   # 自定义异常
│   │
│   └── utils/              # 工具函数
│       ├── validators.py   # 数据验证器
│       └── helpers.py      # 辅助函数
│
├── tests/                  # 测试模块
│   ├── conftest.py         # Pytest 配置和固件
│   ├── test_auth.py        # 认证测试
│   ├── test_service_request.py     # 服务请求测试
│   ├── test_service_response.py    # 服务响应测试
│   ├── test_match.py       # 匹配接受测试
│   ├── test_stats.py       # 统计分析测试
│   └── test_comprehensive_api.py   # 综合 API 测试
│
├── logs/                   # 运行日志
│   └── .gitkeep            # Git 占位符
│
├── run.py                  # 本地开发运行脚本
├── requirements.txt        # Python 依赖
├── pytest.ini              # Pytest 配置
├── Dockerfile              # Docker 镜像定义
├── .gitignore              # Backend 特定的 Git 忽略
└── README.md               # 后端说明文档
```

### frontend/ - Vue 3 前端

前端应用实现用户界面，包括页面、组件、路由和状态管理。

```
frontend/
├── src/                    # 源代码目录
│   ├── main.js             # Vue 应用入口
│   ├── App.vue             # 根组件
│   │
│   ├── views/              # 页面组件
│   │   ├── Home.vue        # 首页
│   │   ├── Login.vue       # 登录页
│   │   ├── Register.vue    # 注册页
│   │   ├── Dashboard.vue   # 用户仪表板
│   │   ├── NeedList.vue    # 服务需求列表
│   │   ├── CreateNeed.vue  # 发布需求
│   │   ├── ServeList.vue   # 服务提供列表
│   │   ├── CreateServe.vue # 发布服务
│   │   ├── MyRequests.vue  # 我的请求
│   │   ├── MyResponses.vue # 我的响应
│   │   └── Statistics.vue  # 统计分析页面
│   │
│   ├── components/         # 可复用组件
│   │   ├── Header.vue      # 头部组件
│   │   ├── Navigation.vue  # 导航组件
│   │   ├── ServiceCard.vue # 服务卡片
│   │   ├── RequestCard.vue # 请求卡片
│   │   ├── StatChart.vue   # 统计图表
│   │   └── ...其他组件
│   │
│   ├── layouts/            # 布局组件
│   │   ├── AppLayout.vue   # 应用主布局
│   │   └── AuthLayout.vue  # 认证布局
│   │
│   ├── router/             # Vue Router 配置
│   │   └── index.js        # 路由定义
│   │
│   ├── stores/             # Pinia 状态管理
│   │   ├── auth.js         # 认证状态
│   │   ├── user.js         # 用户状态
│   │   ├── services.js     # 服务状态
│   │   └── ui.js           # UI 状态
│   │
│   ├── api/                # API 客户端
│   │   ├── index.js        # API 基础配置
│   │   ├── auth.js         # 认证 API
│   │   ├── users.js        # 用户 API
│   │   ├── services.js     # 服务 API
│   │   ├── responses.js    # 响应 API
│   │   └── stats.js        # 统计 API
│   │
│   ├── utils/              # 工具函数
│   │   ├── validators.js   # 表单验证
│   │   ├── helpers.js      # 辅助函数
│   │   └── constants.js    # 常量定义
│   │
│   ├── assets/             # 静态资源
│   │   ├── images/         # 图片
│   │   ├── icons/          # 图标
│   │   └── styles/         # 全局样式
│   │
│   └── App.vue             # 根应用组件
│
├── tests/                  # 测试目录
│   └── e2e/                # E2E 端到端测试
│       ├── auth.spec.ts    # 认证流程测试
│       ├── services.spec.ts # 服务流程测试
│       └── stats.spec.ts   # 统计页面测试
│
├── dist/                   # 生产构建输出（.gitignore）
│   └── .gitkeep
│
├── index.html              # HTML 入口文件
├── package.json            # Node.js 依赖
├── vite.config.js          # Vite 构建配置
├── playwright.config.ts    # Playwright E2E 配置
├── Dockerfile              # Docker 镜像定义
├── nginx.conf              # Nginx 反向代理配置
├── .gitignore              # Frontend 特定的 Git 忽略
└── README.md               # 前端说明文档
```

### database/ - 数据库文件

存储所有与 MySQL 数据库相关的文件。

```
database/
├── schema/                 # 数据库架构
│   ├── goodservices.sql    # 主数据库架构定义
│   │   # 包含：
│   │   # - buser_table: 业务用户表
│   │   # - sr_info: 服务请求表
│   │   # - response_info: 服务响应表
│   │   # - accept_info: 服务接受/完成表
│   │   # - service_type: 服务类型表
│   │   # - city_info: 城市信息表
│   │
│   ├── db_optimization.sql # 数据库优化脚本
│   │   # 包含：
│   │   # - 索引优化
│   │   # - 主键修复
│   │   # - 字段长度调整
│   │
│   └── test_data.sql       # 测试数据初始化
│       # 包含：
│       # - 测试用户数据
│       # - 测试服务请求
│       # - 测试服务响应
│
├── .gitignore              # Database 特定的 Git 忽略
└── README.md               # 数据库说明文档
```

### docs/ - 项目文档

存储项目文档和参考资料。

```
docs/
├── README.md               # 文档索引
├── TECHNICAL_SOLUTION.md   # 技术方案和架构设计
├── DATABASE_DOCUMENTATION.md # 数据库设计文档
├── API_DOCUMENTATION.md    # API 端点参考（如果有手写）
└── requirements.pdf        # 课程项目需求文档
```

### config/ - 配置文件

存储应用配置和部署配置。

```
config/
├── docker-compose.yml      # Docker Compose 编排配置
│   # 定义：
│   # - MySQL 服务
│   # - FastAPI 后端服务
│   # - Vue 前端服务
│   # - Nginx 反向代理
│
├── nginx.conf              # Nginx 反向代理配置
│   # 配置：
│   # - 前端静态文件服务
│   # - 后端 API 代理
│   # - CORS 配置
│
├── deploy.sh               # 部署脚本
│   # 脚本功能：
│   # - 环境检查
│   # - 依赖安装
│   # - 数据库初始化
│   # - 服务启动
│
└── deploy.log.archive      # 部署日志归档
```

### specs/ - 规范和设计文档

存储 API 规范、数据库设计和 LLM 提示词。

```
specs/
├── api/                    # API 规范
│   └── endpoints.md        # API 端点规范文档
│
├── database/               # 数据库规范
│   └── schema.md           # 数据库模式规范
│
└── prompts/                # LLM 提示词模板
    ├── agent-prompts.md    # 各个 Agent 的提示词
    └── task-templates.md   # 任务模板提示词
```

### reports/ - 项目报告

存储课程要求的报告文件。

```
reports/
├── process.md              # 团队进展报告
│   # 内容：
│   # - 团队成员信息
│   # - 任务分工
│   # - 技术栈
│   # - 进度更新
│
└── report.md               # 最终项目报告
    # 内容：
    # - 项目概述
    # - 设计思路
    # - 实现细节
    # - 测试总结
    # - 部署说明
    # - 遇到的问题和解决方案
```

### test-artifacts/ - 测试工件

存储测试运行的结果和输出。

```
test-artifacts/
├── FRONTEND_TEST_RESULTS.md # 前端测试结果汇总
└── frontend-test-results/   # 前端测试详细结果
    ├── artifacts/           # 测试产物（截图、视频等）
    └── html/                # HTML 测试报告
```

## 文件命名约定

### Python 文件
- **模块名**: `snake_case` (例：`service_request.py`)
- **类名**: `PascalCase` (例：`ServiceRequest`)
- **函数名**: `snake_case` (例：`get_service_request()`)
- **常量**: `UPPER_SNAKE_CASE` (例：`MAX_REQUEST_SIZE`)

### Vue 文件
- **单文件组件**: `PascalCase` (例：`ServiceCard.vue`)
- **页面组件**: `PascalCase` (例：`Dashboard.vue`)
- **CSS 类名**: `kebab-case` (例：`service-card`)

### 数据库文件
- **SQL 文件**: `snake_case` (例：`goodservices.sql`)
- **表名**: `snake_case` (例：`service_request`)
- **字段名**: `snake_case` (例：`created_at`)

## 重要文件说明

| 文件路径 | 用途 | 编辑权限 |
|---------|------|--------|
| `README.md` | 项目主要说明 | 管理员 |
| `STRUCTURE.md` | 目录结构指南 | 管理员 |
| `CLAUDE.md` | Claude AI 工作指南 | 管理员 |
| `.gitignore` | Git 忽略配置 | 管理员 |
| `.env.example` | 环境变量模板 | 管理员 |
| `.env` | 实际环境变量 | 不提交 |
| `backend/requirements.txt` | 后端依赖 | 开发者 |
| `frontend/package.json` | 前端依赖 | 开发者 |

## 开发工作流

### 添加新功能

1. **确定文件位置**
   - 后端 API：`backend/app/api/v1/`
   - 后端模型：`backend/app/models/`
   - 前端页面：`frontend/src/views/`
   - 前端组件：`frontend/src/components/`

2. **创建必要的文件**
   - 后端 API：route + schema + crud + model
   - 前端页面：view + API client + router

3. **编写测试**
   - 后端：`backend/tests/test_*.py`
   - 前端：`frontend/tests/e2e/*.spec.ts`

4. **更新文档**
   - 更新 API 文档
   - 更新用户文档

### 提交代码

1. 确保所有文件在正确的位置
2. 验证 .gitignore 正确（不提交 .env, node_modules, venv 等）
3. 提交前运行测试
4. 编写清晰的 commit 信息

## 常见问题

### Q: 我应该在哪里创建新的工具函数？
**A:**
- 后端：`backend/app/utils/helpers.py`
- 前端：`frontend/src/utils/helpers.js`

### Q: 测试文件应该放在哪里？
**A:**
- 后端单元测试：`backend/tests/test_*.py`
- 前端 E2E 测试：`frontend/tests/e2e/*.spec.ts`

### Q: 如何组织新的 API 端点？
**A:**
1. 定义请求/响应模型：`backend/app/schemas/`
2. 定义数据库模型：`backend/app/models/`
3. 实现 CRUD 操作：`backend/app/crud/`
4. 创建路由处理器：`backend/app/api/v1/`

### Q: 为什么有这么多 .gitignore 文件？
**A:** 不同目录有不同的需求：
- 根目录 .gitignore：全局忽略规则
- backend/.gitignore：Python 特定规则
- frontend/.gitignore：Node.js 特定规则
- database/.gitignore：数据库特定规则

## 进一步阅读

- [README.md](README.md) - 项目快速开始指南
- [docs/TECHNICAL_SOLUTION.md](docs/TECHNICAL_SOLUTION.md) - 完整技术方案
- [docs/DATABASE_DOCUMENTATION.md](docs/DATABASE_DOCUMENTATION.md) - 数据库设计
- [CLAUDE.md](CLAUDE.md) - Claude AI 工作指南

---

**最后更新**: 2025-12-16
