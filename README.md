# GoodServices - 社区服务匹配平台

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Node.js](https://img.shields.io/badge/Node.js-16%2B-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)

GoodServices 是一个现代化的社区服务匹配平台，帮助社区居民发布服务需求和提供服务响应。该项目是 Web 开发技术课程的综合实践项目。

## 快速开始

### 项目结构

```
web_full_stack/
├── frontend/               # Vue 3 前端应用
├── backend/                # FastAPI 后端服务
├── database/               # MySQL 数据库文件和文档
├── docs/                   # 项目文档
├── config/                 # Docker 和部署配置
├── specs/                  # API 规范和设计文档
├── reports/                # 项目报告
└── test-artifacts/         # 测试工件和结果
```

详细的目录结构说明，请参考 [STRUCTURE.md](STRUCTURE.md)

### 前置要求

- **Python 3.8+** - 后端开发
- **Node.js 16+** - 前端开发
- **MySQL 8.0+** - 数据库
- **Docker & Docker Compose** (可选) - 容器化部署

### 安装和运行

#### 方式 1：使用 Docker Compose（推荐）

```bash
# 启动所有服务
docker-compose -f config/docker-compose.yml up -d

# 查看日志
docker-compose -f config/docker-compose.yml logs -f

# 停止服务
docker-compose -f config/docker-compose.yml down
```

#### 方式 2：手动设置

**后端设置：**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

# 运行开发服务器
python run.py
```

访问 API 文档：http://localhost:8000/docs

**前端设置：**

```bash
cd frontend
npm install
npm run dev
```

访问应用：http://localhost:5173

### 数据库设置

```bash
# 1. 创建数据库
mysql -u root -p -e "CREATE DATABASE goodservices;"

# 2. 导入架构
mysql -u root -p goodservices < database/schema/goodservices.sql

# 3. （可选）应用优化
mysql -u root -p goodservices < database/schema/db_optimization.sql

# 4. （可选）导入测试数据
mysql -u root -p goodservices < database/schema/test_data.sql
```

## 核心功能

### 1. 用户认证 (Authentication)
- 用户注册和登录
- JWT 令牌认证
- 密码哈希和验证

### 2. 服务请求 (I Need)
- 用户发布服务需求
- 浏览现有请求
- 管理自己的请求

### 3. 服务响应 (I Serve)
- 用户响应服务请求
- 跟踪响应状态
- 接收和拒绝响应

### 4. 服务匹配 (Acceptance)
- 发起者审查响应
- 接受或拒绝响应
- 记录完成的服务

### 5. 统计分析 (Statistics) - 必选功能
- 月度服务统计
- 按服务类型分类统计
- 按城市分类统计
- 数据可视化（ECharts）

## 项目文档

| 文档 | 说明 |
|------|------|
| [technical_solution.md](docs/TECHNICAL_SOLUTION.md) | 完整的技术方案和架构设计 |
| [DATABASE_DOCUMENTATION.md](docs/DATABASE_DOCUMENTATION.md) | 数据库架构和设计文档 |
| [requirements.pdf](docs/requirements.pdf) | 课程项目需求 |
| [CLAUDE.md](CLAUDE.md) | Claude AI 工作指南 |

## 技术栈

### 后端 (Backend)
- **FastAPI** 0.104+ - 现代异步 Web 框架
- **SQLAlchemy** 2.0+ - ORM 对象关系映射
- **Pydantic** 2.x - 数据验证
- **PyJWT** - JWT 认证
- **Passlib + BCrypt** - 密码哈希
- **Uvicorn** - ASGI 服务器

### 前端 (Frontend)
- **Vue 3** - 渐进式 JavaScript 框架
- **Element Plus** - Vue 3 UI 组件库
- **ECharts** - 数据可视化
- **Axios** - HTTP 客户端
- **Pinia** - 状态管理
- **Vue Router** - 单页应用路由

### 数据库
- **MySQL 8.0** - 关系数据库
- **PyMySQL** - Python MySQL 驱动

## API 端点

### 认证 (Authentication)
```
POST   /api/v1/auth/register     - 用户注册
POST   /api/v1/auth/login        - 用户登录
GET    /api/v1/auth/profile      - 获取用户信息
POST   /api/v1/auth/logout       - 登出
```

### 服务请求 (Service Requests)
```
POST   /api/v1/service-requests               - 发布新请求
GET    /api/v1/service-requests               - 查询请求列表
GET    /api/v1/service-requests/{id}          - 获取请求详情
PUT    /api/v1/service-requests/{id}          - 编辑请求
DELETE /api/v1/service-requests/{id}          - 取消请求
```

### 服务响应 (Service Responses)
```
POST   /api/v1/responses                      - 提交响应
GET    /api/v1/responses/{request_id}         - 查询请求的响应
PUT    /api/v1/responses/{response_id}        - 更新响应
DELETE /api/v1/responses/{response_id}        - 删除响应
```

### 服务匹配 (Acceptance)
```
POST   /api/v1/accept/{response_id}           - 接受响应
POST   /api/v1/reject/{response_id}           - 拒绝响应
GET    /api/v1/accept-history                 - 查询完成历史
```

### 统计分析 (Statistics)
```
GET    /api/v1/stats/monthly                  - 月度统计数据
GET    /api/v1/stats/by-service-type          - 按服务类型统计
GET    /api/v1/stats/by-city                  - 按城市统计
```

## 测试

### 后端测试
```bash
cd backend
pytest                          # 运行所有测试
pytest tests/test_auth.py -v   # 运行特定测试
pytest --cov                   # 生成覆盖率报告
```

### 前端 E2E 测试
```bash
cd frontend
npm run test:e2e               # 运行 Playwright E2E 测试
npx playwright show-report     # 查看测试报告
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker-compose -f config/docker-compose.yml build

# 启动容器
docker-compose -f config/docker-compose.yml up -d

# 查看状态
docker-compose -f config/docker-compose.yml ps
```

### 手动部署脚本

```bash
chmod +x config/deploy.sh
./config/deploy.sh
```

## 开发工作流

### 添加新的 API 端点

1. 定义 Pydantic 模型：`backend/app/schemas/`
2. 创建 SQLAlchemy ORM 模型：`backend/app/models/`
3. 实现 CRUD 操作：`backend/app/crud/`
4. 添加路由处理器：`backend/app/api/v1/`
5. 编写测试：`backend/tests/`
6. 查看 Swagger 文档：http://localhost:8000/docs

### 添加新的前端页面

1. 设计 UI：`frontend/src/views/`
2. 添加路由：`frontend/src/router/`
3. 实现 API 调用：`frontend/src/api/`
4. 状态管理：`frontend/src/stores/`

## 问题排查

### 数据库连接失败
- 确保 MySQL 服务正在运行
- 检查 `.env` 文件中的数据库配置
- 验证数据库用户名和密码

### 前后端连接问题
- 检查后端是否在 http://localhost:8000 运行
- 检查 `frontend/src/api/` 中的 API 基础 URL
- 查看浏览器控制台的 CORS 错误

### CORS 错误
- 确保后端配置了正确的 CORS 中间件
- 检查 `backend/app/main.py` 中的 CORS 设置
- 验证前端请求的 Origin

## 课程信息

- **课程名称**: Web 开发技术
- **项目周期**: 第 15-17 周
- **团队成员**: 见 `reports/process.md`
- **交付物**: 源代码 + 数据库备份 + 项目报告

## 许可证

本项目为课程学习用途。

## 联系方式

如有问题或建议，请查看 `reports/process.md` 中的团队联系方式。

---

**最后更新**: 2025-12-16
**项目状态**: 活跃开发中
