# GoodServices 项目 Sub-Agent 体系设计方案

**项目名称：** 好服务（GoodServices）社区服务撮合平台
**文档版本：** v1.0
**编制日期：** 2025-11-17

---

## 目录

1. [Sub-Agent 体系概述](#一subagent-体系概述)
2. [Sub-Agent 详细设计](#二subagent-详细设计)
3. [Agent 协作流程](#三agent-协作流程)
4. [实施方案](#四实施方案)
5. [通信协议](#五通信协议)

---

## 一、Sub-Agent 体系概述

### 1.1 设计理念

采用**微服务化、专业化**的Agent设计理念：
- **单一职责**：每个Agent专注于一个特定领域
- **松耦合**：Agent之间通过标准接口通信
- **可组合**：Agent可以灵活组合完成复杂任务
- **可扩展**：易于添加新的Agent
- **自治性**：每个Agent具有一定的决策能力

### 1.2 Agent 架构图

```
┌────────────────────────────────────────────────────────────────┐
│                      项目管理层 (Orchestrator)                  │
│                  ProjectManagerAgent (总指挥)                   │
└───────────┬────────────────────────────────────────────────────┘
            │
            ├─────────────┬─────────────┬─────────────┬──────────┐
            ↓             ↓             ↓             ↓          ↓
    ┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌──────┐
    │   开发层      │ │  设计层  │ │  测试层  │ │ 文档层  │ │DevOps│
    └──────┬───────┘ └─────┬────┘ └─────┬────┘ └────┬────┘ └───┬──┘
           │               │             │           │          │
    ┌──────┴───────┐   ┌───┴────┐   ┌───┴────┐  ┌──┴───┐   ┌──┴───┐
    ↓              ↓   ↓        ↓   ↓        ↓  ↓      ↓   ↓      ↓
Frontend      Backend  UI    Database API   E2E  API   DB  Deploy Config
Developer     Developer Designer Schema  Tester Tester Doc Doc  Agent  Agent
Agent         Agent    Agent  Agent    Agent  Agent  Agent Agent Agent Agent
```

### 1.3 Agent 清单总览

| 层级 | Agent名称 | 职责 | 优先级 |
|------|----------|------|--------|
| **管理层** | ProjectManagerAgent | 项目总指挥、任务分配、进度跟踪 | P0 |
| **开发层** | FrontendDeveloperAgent | Vue3前端开发 | P0 |
| | BackendDeveloperAgent | FastAPI后端开发 | P0 |
| | DatabaseSchemaAgent | 数据库设计与优化 | P0 |
| **设计层** | UIDesignerAgent | UI/UX设计、原型设计 | P1 |
| | ComponentDesignerAgent | 组件设计与封装 | P1 |
| **测试层** | APITesterAgent | API接口测试 | P0 |
| | E2ETesterAgent | 端到端集成测试 | P0 |
| | PerformanceTesterAgent | 性能测试 | P2 |
| **文档层** | APIDocAgent | API文档编写 | P1 |
| | UserDocAgent | 用户文档/部署文档 | P1 |
| **DevOps层** | DeployAgent | 部署与发布 | P1 |
| | ConfigAgent | 配置管理 | P1 |

---

## 二、Sub-Agent 详细设计

### 2.1 管理层 Agent

#### Agent 1: ProjectManagerAgent (项目经理Agent) ⭐核心

**职责：**
- 项目总体规划与任务分解
- 任务分配给各个子Agent
- 进度跟踪与风险管理
- 协调各Agent协作
- 生成项目报告

**能力：**
- 需求分析能力
- 任务拆分能力
- 资源调度能力
- 进度监控能力
- 决策能力

**输入：**
- 项目需求文档 (`requirements.pdf`)
- 技术方案 (`technical_solution.md`)
- 当前项目状态

**输出：**
- 项目计划 (`project_plan.json`)
- 任务分配表 (`task_assignments.json`)
- 进度报告 (`progress_report.md`)

**工作流程：**
```
1. 读取需求文档和技术方案
2. 分解任务到每个开发阶段
3. 为每个任务分配合适的Agent
4. 监控各Agent执行进度
5. 处理Agent之间的依赖关系
6. 汇总结果生成报告
```

**示例任务分配：**
```json
{
  "phase": "第15周-环境搭建",
  "tasks": [
    {
      "task_id": "TASK-001",
      "name": "数据库优化",
      "assigned_to": "DatabaseSchemaAgent",
      "priority": "P0",
      "estimated_hours": 8,
      "dependencies": []
    },
    {
      "task_id": "TASK-002",
      "name": "后端框架搭建",
      "assigned_to": "BackendDeveloperAgent",
      "priority": "P0",
      "estimated_hours": 16,
      "dependencies": ["TASK-001"]
    },
    {
      "task_id": "TASK-003",
      "name": "前端框架搭建",
      "assigned_to": "FrontendDeveloperAgent",
      "priority": "P0",
      "estimated_hours": 8,
      "dependencies": []
    }
  ]
}
```

---

### 2.2 开发层 Agent

#### Agent 2: FrontendDeveloperAgent (前端开发Agent) ⭐核心

**职责：**
- Vue 3 + Element Plus 前端开发
- 组件开发与页面实现
- 状态管理（Pinia）
- 路由配置（Vue Router）
- API接口调用

**技术栈：**
- Vue 3 (Composition API)
- Element Plus
- ECharts (数据可视化)
- Axios (HTTP客户端)
- Pinia (状态管理)

**输入：**
- UI设计稿（来自UIDesignerAgent）
- API接口文档（来自BackendDeveloperAgent）
- 组件设计方案（来自ComponentDesignerAgent）

**输出：**
- 前端页面代码 (`frontend/src/views/`)
- 公共组件 (`frontend/src/components/`)
- API封装 (`frontend/src/api/`)
- 路由配置 (`frontend/src/router/`)

**核心任务列表：**

1. **基础架构搭建**
   - 初始化Vite项目
   - 配置Vue Router
   - 配置Pinia Store
   - 配置Axios拦截器
   - 设计主布局（Header + Sidebar + Content）

2. **页面开发（按优先级）**
   - P0: 登录注册页面 (`views/auth/`)
   - P0: 用户中心页面 (`views/user/`)
   - P0: "我需要"模块 (`views/needs/`)
   - P0: "我服务"模块 (`views/responses/`)
   - P0: 统计分析页面 (`views/stats/`) ⭐必选
   - P1: 管理员页面 (`views/admin/`)

3. **公共组件开发**
   - 分页组件 (`Pagination.vue`)
   - 文件上传组件 (`FileUpload.vue`)
   - 日期选择器封装
   - 确认对话框封装

4. **状态管理**
   - 用户状态 (userStore)
   - 全局配置状态 (configStore)

5. **数据可视化**
   - ECharts折线图组件
   - 统计数据展示

**代码示例（关键结构）：**
```javascript
// src/api/auth.js
import request from '@/utils/request'

export const login = (data) => {
  return request({
    url: '/api/v1/auth/login',
    method: 'post',
    data
  })
}

// src/stores/user.js
import { defineStore } from 'pinia'
import { login } from '@/api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: {}
  }),
  actions: {
    async login(credentials) {
      const res = await login(credentials)
      this.token = res.data.token
      this.userInfo = res.data.user_info
      localStorage.setItem('token', this.token)
    }
  }
})
```

**质量标准：**
- 代码符合Vue 3风格指南
- 组件可复用性高
- 响应式设计（适配移动端）
- 错误处理完善
- 加载状态提示

---

#### Agent 3: BackendDeveloperAgent (后端开发Agent) ⭐核心

**职责：**
- FastAPI + SQLAlchemy 后端开发
- RESTful API设计与实现
- 数据库CRUD操作
- JWT认证授权
- 业务逻辑实现

**技术栈：**
- FastAPI (Web框架)
- SQLAlchemy (ORM)
- Pydantic (数据验证)
- python-jose (JWT)
- Passlib (密码加密)

**输入：**
- 数据库Schema（来自DatabaseSchemaAgent）
- API接口规范（来自ProjectManagerAgent）
- 业务需求文档

**输出：**
- 后端代码 (`backend/app/`)
- API接口（RESTful）
- 数据库模型 (`app/models/`)
- Swagger文档（自动生成）

**核心任务列表：**

1. **基础架构搭建**
   - 创建FastAPI应用 (`main.py`)
   - 配置数据库连接 (`database.py`)
   - 配置CORS中间件
   - 配置JWT认证 (`core/security.py`)
   - 依赖注入设计 (`dependencies.py`)

2. **数据模型开发** (`app/models/`)
   - BUser (用户模型)
   - ServiceRequest (服务需求模型)
   - ServiceResponse (服务响应模型)
   - AcceptInfo (服务达成模型)
   - ServiceType, CityInfo (字典表)
   - Report (统计报表)

3. **Schema设计** (`app/schemas/`)
   - 请求Schema（数据验证）
   - 响应Schema（数据序列化）
   - 分页Schema

4. **CRUD层开发** (`app/crud/`)
   - 用户CRUD
   - 服务需求CRUD
   - 服务响应CRUD
   - 统计查询

5. **API路由开发** (`app/api/v1/`)
   - `/auth` - 认证接口（注册、登录）
   - `/users` - 用户管理
   - `/service-requests` - 服务需求
   - `/service-responses` - 服务响应
   - `/match` - 服务撮合
   - `/stats` - 统计分析 ⭐必选

6. **关键功能实现**
   - 密码校验（至少6位、至少2个数字、不能全大小写）
   - JWT Token生成与验证
   - 分页查询
   - 事务处理（服务撮合）
   - 月度统计查询

**代码示例（关键实现）：**
```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import UserRegister, UserLogin
from app.crud import user as crud_user
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    """用户注册 - Pydantic自动验证"""
    # 检查用户名是否存在
    if crud_user.get_user_by_username(db, user.uname):
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 创建用户
    new_user = crud_user.create_user(db, user)
    return {"code": 200, "message": "注册成功", "data": {"user_id": new_user.id}}

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = crud_user.authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 生成JWT Token
    token = create_access_token(data={"sub": str(user.id), "username": user.uname})
    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "token": token,
            "user_info": {"id": user.id, "uname": user.uname, "bname": user.bname}
        }
    }
```

**质量标准：**
- 符合RESTful规范
- 完善的错误处理
- 自动生成Swagger文档
- 数据验证完整
- 事务安全

---

#### Agent 4: DatabaseSchemaAgent (数据库架构Agent)

**职责：**
- 数据库Schema设计与优化
- SQL脚本编写
- 索引设计
- 数据库迁移管理（Alembic）

**技术栈：**
- MySQL 8.0
- Alembic (数据库迁移)
- SQLAlchemy (ORM)

**输入：**
- 业务需求文档
- 数据模型设计
- 现有数据库Schema (`goodservices.sql`)

**输出：**
- 优化后的SQL脚本 (`db_optimization.sql`)
- 测试数据脚本 (`test_data.sql`)
- 数据库文档 (已有 `goodservices_database_documentation.md`)
- Alembic迁移脚本

**核心任务列表：**

1. **数据库优化**
   - 修复report表主键问题（改为复合主键）
   - 添加唯一约束（uname, phoneNo, idno）
   - 修改字段类型（response_info.desc改为VARCHAR）
   - 修改密码字段长度（支持BCrypt）

2. **索引设计**
   - 添加查询优化索引
   - 外键索引
   - 联合索引

3. **测试数据准备**
   - 用户测试数据
   - 服务需求测试数据
   - 服务响应测试数据
   - 月度统计测试数据

4. **数据库迁移**
   - 配置Alembic
   - 生成迁移脚本
   - 版本管理

**输出示例：**
```sql
-- db_optimization.sql
-- 1. 修复 report 表主键
ALTER TABLE report DROP PRIMARY KEY;
ALTER TABLE report ADD PRIMARY KEY (monthID, stype_id, cityID);

-- 2. 添加唯一约束
ALTER TABLE buser_table ADD UNIQUE KEY uk_uname (uname);
ALTER TABLE buser_table ADD UNIQUE KEY uk_phoneNo (phoneNo);

-- 3. 添加索引
CREATE INDEX idx_sr_state ON sr_info(ps_state, ps_begindate);
CREATE INDEX idx_sr_city_type ON sr_info(cityID, stype_id);
```

---

### 2.3 设计层 Agent

#### Agent 5: UIDesignerAgent (UI设计Agent)

**职责：**
- 页面UI设计
- 交互流程设计
- 组件设计规范
- 响应式布局设计

**设计工具：**
- Element Plus 组件库
- 颜色规范
- 字体规范
- 间距规范

**输入：**
- 需求文档
- 功能模块清单

**输出：**
- 页面设计稿（Markdown描述）
- 组件设计规范 (`ui_design_spec.md`)
- 交互流程图
- 颜色/字体规范

**核心任务列表：**

1. **主题设计**
   - 主色调：Element Plus默认蓝色 `#409EFF`
   - 成功色：绿色 `#67C23A`
   - 警告色：橙色 `#E6A23C`
   - 危险色：红色 `#F56C6C`

2. **布局设计**
   - 顶部导航栏（Logo + 导航菜单 + 用户信息）
   - 侧边栏（功能菜单）
   - 主内容区（动态路由）
   - 面包屑导航

3. **关键页面设计**
   - 登录页：居中卡片式
   - 注册页：表单验证提示
   - "我需要"列表页：卡片式 + 分页
   - 统计分析页：图表 + 表格

4. **组件规范**
   - 按钮：主要/次要/危险
   - 表单：标签宽度、必填标识
   - 表格：斑马纹、边框
   - 对话框：统一宽度

**输出示例：**
```markdown
# 统计分析页面设计

## 布局结构
- 顶部：查询条件表单（起始月份、终止月份、城市、服务类型）
- 中部：ECharts折线图（高度400px）
- 底部：数据明细表格 + 分页

## 交互设计
- 点击"查询"按钮：加载Loading，请求数据，渲染图表和表格
- 图表支持缩放、数据标签hover展示
- 表格支持排序（按发布数、成功数）

## 颜色方案
- 发布需求数曲线：蓝色 #409EFF
- 响应成功数曲线：绿色 #67C23A
```

---

#### Agent 6: ComponentDesignerAgent (组件设计Agent)

**职责：**
- 封装可复用组件
- 组件API设计
- 组件文档编写

**输入：**
- 页面设计稿
- 重复出现的UI模式

**输出：**
- 公共组件代码 (`components/`)
- 组件使用文档

**核心任务列表：**

1. **基础组件封装**
   - `Pagination.vue` - 分页组件
   - `ConfirmDialog.vue` - 确认对话框
   - `FileUpload.vue` - 文件上传
   - `DateRangePicker.vue` - 日期范围选择

2. **业务组件封装**
   - `ServiceRequestCard.vue` - 服务需求卡片
   - `ServiceResponseCard.vue` - 服务响应卡片
   - `StatisticsChart.vue` - 统计图表

**组件示例：**
```vue
<!-- components/Pagination.vue -->
<template>
  <div class="pagination-container">
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      @current-change="handlePageChange"
      @size-change="handleSizeChange"
    />
  </div>
</template>

<script setup>
const props = defineProps({
  total: { type: Number, required: true },
  modelValue: { type: Object, required: true } // { page, size }
})

const emit = defineEmits(['update:modelValue', 'change'])

const currentPage = computed({
  get: () => props.modelValue.page,
  set: (val) => emit('update:modelValue', { ...props.modelValue, page: val })
})

const pageSize = computed({
  get: () => props.modelValue.size,
  set: (val) => emit('update:modelValue', { ...props.modelValue, size: val })
})

const handlePageChange = (page) => {
  emit('change', { page, size: pageSize.value })
}

const handleSizeChange = (size) => {
  emit('change', { page: 1, size })
}
</script>
```

---

### 2.4 测试层 Agent

#### Agent 7: APITesterAgent (API测试Agent) ⭐核心

**职责：**
- API接口自动化测试
- 接口功能验证
- 边界条件测试
- 生成测试报告

**测试工具：**
- pytest (Python测试框架)
- httpx (异步HTTP客户端)
- Postman (手动测试)

**输入：**
- API接口列表（来自BackendDeveloperAgent）
- Swagger文档 (http://localhost:8000/docs)
- 测试用例设计

**输出：**
- 测试代码 (`tests/test_api.py`)
- 测试报告 (`test_report.html`)
- Bug清单 (`bugs.md`)

**核心任务列表：**

1. **认证模块测试**
   - 用户注册（正常、异常）
   - 用户登录（正常、密码错误）
   - 密码校验规则测试

2. **用户模块测试**
   - 获取用户信息（需要Token）
   - 修改用户信息
   - 修改密码

3. **服务需求模块测试**
   - 发布需求（CRUD）
   - 分页查询
   - 权限验证

4. **服务响应模块测试**
   - 提交响应（CRUD）
   - 分页查询

5. **服务撮合模块测试**
   - 接受响应（事务测试）
   - 拒绝响应

6. **统计分析模块测试** ⭐必选
   - 月度统计查询
   - 参数验证

**测试代码示例：**
```python
# tests/test_api.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_user_register():
    """测试用户注册"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # 正常注册
        response = await client.post("/api/v1/auth/register", json={
            "uname": "testuser",
            "ctype": "身份证",
            "idno": "110101199001011234",
            "bname": "测试用户",
            "bpwd": "Pass123",
            "phoneNo": "13800138000",
            "desc": "测试"
        })
        assert response.status_code == 200
        assert response.json()["code"] == 200

        # 密码校验失败：少于6位
        response = await client.post("/api/v1/auth/register", json={
            "uname": "testuser2",
            "bpwd": "Pass1",  # 只有5位
            # ... 其他字段
        })
        assert response.status_code == 422  # Pydantic验证失败

        # 密码校验失败：数字少于2个
        response = await client.post("/api/v1/auth/register", json={
            "uname": "testuser3",
            "bpwd": "Password1",  # 只有1个数字
            # ... 其他字段
        })
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_user_login():
    """测试用户登录"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # 正确登录
        response = await client.post("/api/v1/auth/login", json={
            "username": "testuser",
            "password": "Pass123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "token" in data["data"]

        # 错误密码
        response = await client.post("/api/v1/auth/login", json={
            "username": "testuser",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
```

**测试报告格式：**
```markdown
# API测试报告

**测试时间：** 2025-11-17 14:30
**测试范围：** 所有API接口
**测试结果：** 45个测试用例，43个通过，2个失败

## 测试统计
- 认证模块：✅ 8/8
- 用户模块：✅ 5/5
- 服务需求模块：✅ 12/12
- 服务响应模块：✅ 10/10
- 服务撮合模块：⚠️ 4/6 (2个失败)
- 统计分析模块：✅ 4/4

## 失败用例
1. `test_accept_response_concurrent` - 并发接受响应时出现数据不一致
2. `test_accept_response_transaction` - 事务回滚未生效

## 建议
- 服务撮合模块需要添加数据库锁机制
- 增加并发测试用例
```

---

#### Agent 8: E2ETesterAgent (端到端测试Agent)

**职责：**
- 前后端集成测试
- 完整业务流程测试
- UI自动化测试（可选）

**测试工具：**
- Playwright (前端E2E测试)
- Selenium (可选)

**输入：**
- 完整功能系统
- 业务流程清单

**输出：**
- E2E测试脚本 (`tests/e2e/`)
- 测试报告
- 视频录制（测试过程）

**核心测试场景：**

1. **用户注册登录流程**
   - 注册新用户 → 登录 → 查看个人信息

2. **发布服务需求流程**
   - 登录 → 发布需求 → 查看我的需求列表

3. **响应服务需求流程**
   - 登录 → 浏览需求 → 提交响应 → 查看我的响应

4. **服务撮合流程** ⭐核心
   - 用户A发布需求 → 用户B响应 → 用户A接受 → 验证服务达成记录

5. **统计分析流程** ⭐必选
   - 登录 → 进入统计页面 → 选择条件 → 查看图表和表格

**E2E测试代码示例（Playwright）：**
```javascript
// tests/e2e/service-match.spec.js
import { test, expect } from '@playwright/test'

test('完整服务撮合流程', async ({ page }) => {
  // 1. 用户A登录
  await page.goto('http://localhost:5173/login')
  await page.fill('input[name="username"]', 'zhangsan')
  await page.fill('input[name="password"]', 'Pass123')
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL(/.*home/)

  // 2. 用户A发布需求
  await page.click('text=我需要')
  await page.click('text=发布需求')
  await page.fill('input[name="title"]', '厨房水管漏水')
  await page.selectOption('select[name="serviceType"]', '1') // 管道维修
  await page.fill('textarea[name="desc"]', '水管破裂需要维修')
  await page.click('button:has-text("提交")')
  await expect(page.locator('.el-message--success')).toBeVisible()

  // 3. 用户A登出，用户B登录
  await page.click('.user-avatar')
  await page.click('text=退出登录')
  await page.goto('http://localhost:5173/login')
  await page.fill('input[name="username"]', 'lisi')
  await page.fill('input[name="password"]', 'Pass456')
  await page.click('button[type="submit"]')

  // 4. 用户B响应需求
  await page.click('text=我服务')
  await page.click('.service-card:has-text("厨房水管漏水")')
  await page.click('button:has-text("我服务")')
  await page.fill('input[name="title"]', '专业水管维修')
  await page.fill('textarea[name="desc"]', '30分钟上门')
  await page.click('button:has-text("提交响应")')
  await expect(page.locator('.el-message--success')).toBeVisible()

  // 5. 用户B登出，用户A登录
  await page.click('.user-avatar')
  await page.click('text=退出登录')
  // ... 登录用户A

  // 6. 用户A接受响应
  await page.click('text=我需要')
  await page.click('.service-card:has-text("厨房水管漏水")')
  await page.click('button:has-text("查看响应")')
  await page.click('button:has-text("接受"):first')
  await expect(page.locator('.el-message-box')).toBeVisible()
  await page.click('button:has-text("确定")')
  await expect(page.locator('.el-message--success')).toHaveText(/接受成功/)

  // 7. 验证服务达成记录
  await page.click('text=服务记录')
  await expect(page.locator('table')).toContainText('厨房水管漏水')
})
```

---

#### Agent 9: PerformanceTesterAgent (性能测试Agent)

**职责：**
- 接口性能测试
- 并发压力测试
- 数据库查询优化建议

**测试工具：**
- Locust (Python性能测试)
- Apache JMeter (可选)

**输入：**
- 关键API接口
- 性能指标要求

**输出：**
- 性能测试报告 (`performance_report.md`)
- 优化建议

**测试场景：**
- 登录接口并发测试（100用户/秒）
- 查询接口并发测试（200请求/秒）
- 分页查询性能测试（大数据量）

---

### 2.5 文档层 Agent

#### Agent 10: APIDocAgent (API文档Agent)

**职责：**
- 编写API接口文档
- 维护Swagger文档
- 生成Postman Collection

**输入：**
- FastAPI代码（自动生成Swagger）
- 额外说明信息

**输出：**
- API文档 (`api_documentation.md`)
- Swagger JSON导出
- Postman Collection

**任务：**
- 补充Swagger文档中的描述
- 添加请求/响应示例
- 编写错误码说明
- 生成Markdown格式API文档

---

#### Agent 11: UserDocAgent (用户文档Agent)

**职责：**
- 编写用户使用文档
- 编写部署文档
- 编写开发文档

**输出：**
- 用户手册 (`user_manual.md`)
- 部署文档 (`deployment_guide.md`)
- 开发文档 (`development_guide.md`)
- 项目报告（课程要求）

**核心文档：**

1. **用户手册**
   - 系统介绍
   - 功能使用说明（含截图）
   - 常见问题FAQ

2. **部署文档**
   - 环境要求
   - 安装步骤
   - 配置说明
   - 故障排除

3. **开发文档**
   - 项目结构
   - 技术栈说明
   - 代码规范
   - 开发流程

4. **项目报告**（课程要求）
   - 运行环境配置说明
   - 已实现功能清单
   - 未实现功能清单
   - 额外添加的功能
   - 关键界面截图
   - 类交互设计说明
   - 小组分工说明

---

### 2.6 DevOps层 Agent

#### Agent 12: DeployAgent (部署Agent)

**职责：**
- 自动化部署
- 环境配置
- 服务启动

**工具：**
- Docker (容器化)
- Docker Compose (编排)

**输入：**
- 前端代码
- 后端代码
- 配置文件

**输出：**
- Dockerfile
- docker-compose.yml
- 部署脚本 (`deploy.sh`)

**部署方案示例：**
```yaml
# docker-compose.yml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: goodservices
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./goodservices.sql:/docker-entrypoint-initdb.d/init.sql

  backend:
    build: ./backend
    environment:
      DATABASE_URL: mysql+pymysql://root:password@mysql:3306/goodservices
    ports:
      - "8000:8000"
    depends_on:
      - mysql

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  mysql_data:
```

---

#### Agent 13: ConfigAgent (配置管理Agent)

**职责：**
- 管理环境配置
- 生成配置文件
- 配置验证

**输出：**
- `.env` 配置文件
- `config.py` 配置类
- 配置文档

---

## 三、Agent 协作流程

### 3.1 整体开发流程

```
阶段1: 项目初始化（第15周）
ProjectManagerAgent
    ├─> DatabaseSchemaAgent: 数据库优化
    ├─> BackendDeveloperAgent: 后端框架搭建
    ├─> FrontendDeveloperAgent: 前端框架搭建
    └─> ConfigAgent: 配置管理

阶段2: 核心功能开发（第16周）
ProjectManagerAgent
    ├─> UIDesignerAgent: 页面设计
    │       └─> FrontendDeveloperAgent: 页面开发
    ├─> BackendDeveloperAgent: API开发
    │       └─> APITesterAgent: API测试
    └─> ComponentDesignerAgent: 组件封装

阶段3: 集成测试与文档（第17周）
ProjectManagerAgent
    ├─> E2ETesterAgent: 端到端测试
    ├─> PerformanceTesterAgent: 性能测试
    ├─> APIDocAgent: API文档
    ├─> UserDocAgent: 用户文档
    └─> DeployAgent: 部署发布
```

### 3.2 典型协作场景

#### 场景1：开发"统计分析"模块

```
1. ProjectManagerAgent 分配任务
   ↓
2. UIDesignerAgent 设计统计页面UI
   - 输出：页面设计稿（查询表单 + ECharts图表 + 数据表格）
   ↓
3. BackendDeveloperAgent 开发统计API
   - 输入：数据库Schema
   - 开发：`/api/v1/stats/monthly` 接口
   - 输出：API接口 + Swagger文档
   ↓
4. APITesterAgent 测试统计API
   - 测试：参数验证、数据正确性
   - 输出：测试报告
   ↓
5. FrontendDeveloperAgent 开发统计页面
   - 输入：UI设计稿 + API文档
   - 开发：查询表单 + ECharts集成 + 数据表格
   - 输出：Statistics.vue
   ↓
6. E2ETesterAgent 端到端测试
   - 测试：完整流程（登录 → 查询 → 图表展示）
   - 输出：E2E测试报告
   ↓
7. ProjectManagerAgent 验收
   - 检查：功能完整性、用户体验
   - 结果：通过/需要修改
```

#### 场景2：发现Bug修复流程

```
1. APITesterAgent 发现Bug
   - Bug：并发接受响应时数据不一致
   ↓
2. ProjectManagerAgent 分配给 BackendDeveloperAgent
   ↓
3. BackendDeveloperAgent 修复Bug
   - 添加数据库锁机制
   - 修改服务撮合接口
   ↓
4. APITesterAgent 重新测试
   - 验证Bug已修复
   ↓
5. E2ETesterAgent 回归测试
   - 确保其他功能未受影响
```

---

## 四、实施方案

### 4.1 Agent实现方式

#### 方式1：人工扮演Agent角色（适合小团队）

**适用场景：** 3人团队，手动分工

**实施：**
- 每个人承担多个Agent角色
- 使用文档沟通（Markdown文件作为交付物）
- 使用Git管理代码和文档

**角色分配示例：**
- **成员A（后端负责人）**
  - ProjectManagerAgent (20%)
  - BackendDeveloperAgent (50%)
  - DatabaseSchemaAgent (20%)
  - APITesterAgent (10%)

- **成员B（后端开发）**
  - BackendDeveloperAgent (60%)
  - APIDocAgent (20%)
  - ConfigAgent (20%)

- **成员C（前端+测试）**
  - FrontendDeveloperAgent (50%)
  - UIDesignerAgent (20%)
  - E2ETesterAgent (20%)
  - UserDocAgent (10%)

---

#### 方式2：半自动化Agent（推荐）

**适用场景：** 有AI辅助工具（Claude Code、GitHub Copilot）

**实施：**
- 使用AI辅助代码生成
- 人工负责审查和决策
- 自动化测试和部署

**工具组合：**
- **代码生成：** Claude Code / GitHub Copilot
- **测试：** pytest (自动) + 手动验收
- **部署：** Docker Compose (自动)
- **文档：** AI辅助生成 + 人工完善

**工作流程：**
```bash
# 示例：开发认证模块
1. 人工：定义需求 → "开发用户注册接口，包含密码校验"
2. AI Agent：生成代码
   - 生成 app/api/v1/auth.py
   - 生成 app/schemas/auth.py (含密码校验validator)
   - 生成 app/crud/user.py
3. 人工：代码审查 → 修改细节
4. AI Agent：生成测试代码
   - 生成 tests/test_auth.py
5. 自动化：运行测试 → pytest
6. 人工：验收 → 合并代码
```

---

#### 方式3：全自动化Multi-Agent系统（未来方向）

**适用场景：** 研究项目、大型团队

**实施：**
- 使用LangChain/AutoGPT构建Agent系统
- Agent之间自动通信和协作
- 人工仅负责最终验收

**架构：**
```python
# 伪代码示例
from langchain.agents import Agent, AgentExecutor

# 创建各个Agent
project_manager = Agent(
    name="ProjectManager",
    role="项目经理",
    tools=["task_allocator", "progress_tracker"]
)

backend_dev = Agent(
    name="BackendDeveloper",
    role="后端开发",
    tools=["fastapi_generator", "sqlalchemy_orm", "git"]
)

frontend_dev = Agent(
    name="FrontendDeveloper",
    role="前端开发",
    tools=["vue_generator", "element_plus", "git"]
)

# 创建Agent执行器
executor = AgentExecutor(
    agents=[project_manager, backend_dev, frontend_dev],
    communication_protocol="message_queue"
)

# 执行任务
executor.run("开发好服务平台的用户注册功能")
```

---

### 4.2 实施步骤（基于方式2：半自动化）

#### 第15周：环境搭建与基础架构

**Day 1-2: 项目初始化**
```bash
# ProjectManagerAgent + ConfigAgent
1. 创建项目目录结构
mkdir -p backend/app/{api,models,schemas,crud,core,utils}
mkdir -p frontend/src/{views,components,api,stores,router}

2. 初始化Git仓库
git init
git add .
git commit -m "feat: 项目初始化"

3. 配置开发环境
python -m venv venv
npm create vite@latest frontend -- --template vue
```

**Day 3: 数据库优化**
```bash
# DatabaseSchemaAgent
1. 执行数据库优化脚本
mysql -u root -p goodservices < db_optimization.sql

2. 导入测试数据
mysql -u root -p goodservices < test_data.sql

3. 验证数据
mysql -u root -p goodservices -e "SHOW TABLES;"
```

**Day 4-5: 后端框架搭建**
```bash
# BackendDeveloperAgent
1. 创建FastAPI应用
# 使用AI生成 app/main.py, app/database.py

2. 创建数据库模型
# 使用AI根据goodservices.sql生成SQLAlchemy模型

3. 配置JWT认证
# 使用AI生成 app/core/security.py

4. 测试Swagger文档
uvicorn app.main:app --reload
# 访问 http://localhost:8000/docs
```

**Day 6: 前端框架搭建**
```bash
# FrontendDeveloperAgent
1. 配置路由和状态管理
# 使用AI生成 src/router/index.js, src/stores/user.js

2. 配置Axios拦截器
# 使用AI生成 src/utils/request.js

3. 设计主布局
# 使用AI生成 src/layouts/MainLayout.vue
```

---

#### 第16周：核心功能开发

**Day 1-2: 认证模块**
```bash
# BackendDeveloperAgent + FrontendDeveloperAgent
后端：
- app/api/v1/auth.py (注册、登录接口)
- app/schemas/auth.py (含密码校验validator)

前端：
- src/views/auth/Login.vue
- src/views/auth/Register.vue

测试：
# APITesterAgent
pytest tests/test_auth.py
```

**Day 3-4: "我需要"模块**
```bash
# BackendDeveloperAgent + FrontendDeveloperAgent
后端：
- app/api/v1/service_request.py (CRUD + 分页)
- app/models/service_request.py

前端：
- src/views/needs/MyNeeds.vue (列表)
- src/views/needs/CreateNeed.vue (发布)
- src/views/needs/NeedDetail.vue (详情)

测试：
pytest tests/test_service_request.py
```

**Day 5-6: "我服务"模块 + 服务撮合**
```bash
# 类似"我需要"模块
后端：service_response.py, match.py
前端：MyResponses.vue, CreateResponse.vue
```

---

#### 第17周：统计分析 + 测试 + 文档

**Day 1-3: 统计分析模块** ⭐必选
```bash
# UIDesignerAgent → BackendDeveloperAgent → FrontendDeveloperAgent
1. UI设计
   - 查询表单 + ECharts图表 + 数据表格

2. 后端开发
   - app/api/v1/stats.py (月度统计查询)

3. 前端开发
   - src/views/stats/Statistics.vue
   - 集成ECharts折线图

4. 测试
   pytest tests/test_stats.py
   Playwright E2E测试
```

**Day 4-5: 集成测试与Bug修复**
```bash
# E2ETesterAgent + 全员
1. 端到端测试
   playwright test tests/e2e/

2. 性能测试
   locust -f tests/performance/locustfile.py

3. Bug修复
   # 根据测试报告修复问题
```

**Day 6-7: 文档编写与部署**
```bash
# UserDocAgent + DeployAgent
1. 编写项目报告
   - 运行环境配置说明
   - 已实现功能清单
   - 关键界面截图
   - 小组分工说明

2. 导出数据库
   mysqldump -u root -p goodservices > sql.txt

3. 打包提交
   zip -r 姓名1_姓名2_姓名3.zip frontend/ backend/ sql.txt 报告.docx
```

---

### 4.3 工具与模板

#### 任务模板 (`task_template.md`)

```markdown
# Task: [任务名称]

**Task ID:** TASK-XXX
**Assigned Agent:** [Agent名称]
**Priority:** P0/P1/P2
**Estimated Hours:** X hours
**Dependencies:** [前置任务]

## 目标
[任务目标描述]

## 输入
- [输入文件1]
- [输入文件2]

## 输出
- [输出文件1]
- [输出文件2]

## 验收标准
- [ ] 标准1
- [ ] 标准2
- [ ] 标准3

## 实施步骤
1. 步骤1
2. 步骤2
3. 步骤3

## 风险
- 风险1：[应对措施]
- 风险2：[应对措施]
```

#### 交付物检查清单 (`deliverable_checklist.md`)

```markdown
# 交付物检查清单

## 代码
- [ ] 前端代码 (frontend/)
- [ ] 后端代码 (backend/)
- [ ] 代码符合规范
- [ ] 无明显Bug

## 测试
- [ ] API测试通过（pytest）
- [ ] E2E测试通过（Playwright）
- [ ] 测试报告生成

## 文档
- [ ] API文档（Swagger）
- [ ] 用户文档
- [ ] 部署文档
- [ ] 项目报告

## 数据库
- [ ] 数据库SQL文件 (sql.txt)
- [ ] 测试数据

## 配置
- [ ] requirements.txt
- [ ] package.json
- [ ] .env.example
```

---

## 五、通信协议

### 5.1 Agent间消息格式

```json
{
  "message_id": "MSG-20251117-001",
  "from_agent": "BackendDeveloperAgent",
  "to_agent": "APITesterAgent",
  "timestamp": "2025-11-17T10:30:00Z",
  "message_type": "TASK_COMPLETED",
  "content": {
    "task_id": "TASK-002",
    "status": "completed",
    "deliverables": [
      "app/api/v1/auth.py",
      "app/schemas/auth.py"
    ],
    "notes": "认证接口开发完成，Swagger文档已自动生成",
    "next_action": "请进行API测试"
  }
}
```

### 5.2 状态同步机制

**方式1：文件系统同步**
```bash
# 使用JSON文件记录任务状态
project_status.json
task_assignments.json
agent_outputs/
    ├── backend/
    ├── frontend/
    └── tests/
```

**方式2：Git Commit消息**
```bash
# 使用Git作为通信媒介
git commit -m "feat(backend): 完成认证模块开发 [BackendDeveloperAgent] → [APITesterAgent]"
```

---

## 六、总结

### 6.1 Sub-Agent体系优势

1. **专业化分工**：每个Agent专注于特定领域，提高质量
2. **并行开发**：多个Agent可同时工作，提高效率
3. **可追溯**：每个Agent的输出都有记录，便于审查
4. **可扩展**：易于添加新的Agent（如SecurityAgent、MonitorAgent）
5. **降低复杂度**：将大任务拆解为小任务，逐个攻克

### 6.2 关键成功因素

✅ **ProjectManagerAgent的协调能力**：任务分配合理、进度跟踪及时
✅ **Agent间清晰的接口定义**：输入输出明确、交付标准清晰
✅ **自动化测试覆盖**：APITesterAgent、E2ETesterAgent保证质量
✅ **文档驱动**：每个Agent都有明确的文档输出
✅ **持续集成**：使用Git + 自动化测试保证代码质量

### 6.3 实施建议

**第一步：** 建立ProjectManagerAgent（人工担任），制定详细的任务计划
**第二步：** 搭建基础架构（数据库、后端框架、前端框架）
**第三步：** 并行开发核心模块（认证、需求、响应）
**第四步：** 开发统计分析模块（必选，重点）
**第五步：** 全面测试与文档编写
**第六步：** 部署与验收

---

**文档版本：** v1.0
**编制日期：** 2025-11-17
**编制人：** Claude Code

---

## 附录：Agent技能卡片

### BackendDeveloperAgent 技能卡片

```
┌────────────────────────────────────────────┐
│   BackendDeveloperAgent (后端开发专家)    │
├────────────────────────────────────────────┤
│ 🎯 核心技能                                │
│   • FastAPI框架开发                        │
│   • SQLAlchemy ORM                         │
│   • Pydantic数据验证                       │
│   • JWT认证                                │
│   • RESTful API设计                        │
│                                            │
│ 📥 输入                                    │
│   • 数据库Schema                           │
│   • API接口规范                            │
│   • 业务需求文档                           │
│                                            │
│ 📤 输出                                    │
│   • Python代码 (app/)                      │
│   • Swagger文档 (/docs)                   │
│   • API接口 (RESTful)                      │
│                                            │
│ ⚡ 工作流程                                 │
│   1. 分析需求 → 2. 设计API →               │
│   3. 编写代码 → 4. 自测 →                  │
│   5. 提交 → 6. 协作测试                    │
│                                            │
│ 🔧 工具                                    │
│   Python 3.10, FastAPI, SQLAlchemy,       │
│   Pydantic, PyMySQL, pytest               │
└────────────────────────────────────────────┘
```

### FrontendDeveloperAgent 技能卡片

```
┌────────────────────────────────────────────┐
│   FrontendDeveloperAgent (前端开发专家)   │
├────────────────────────────────────────────┤
│ 🎯 核心技能                                │
│   • Vue 3 Composition API                  │
│   • Element Plus组件库                     │
│   • ECharts数据可视化                      │
│   • Pinia状态管理                          │
│   • Axios HTTP请求                         │
│                                            │
│ 📥 输入                                    │
│   • UI设计稿                               │
│   • API接口文档                            │
│   • 组件设计方案                           │
│                                            │
│ 📤 输出                                    │
│   • Vue组件 (src/views/, src/components/) │
│   • 路由配置 (src/router/)                │
│   • API封装 (src/api/)                    │
│                                            │
│ ⚡ 工作流程                                 │
│   1. 理解设计 → 2. 开发组件 →              │
│   3. 对接API → 4. 自测 →                   │
│   5. 提交 → 6. 协作测试                    │
│                                            │
│ 🔧 工具                                    │
│   Node.js, Vue 3, Vite, Element Plus,     │
│   ECharts, Axios, Pinia                    │
└────────────────────────────────────────────┘
```

---

**祝GoodServices项目开发顺利！🚀**
