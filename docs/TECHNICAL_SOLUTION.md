# GoodServices 平台技术方案文档（Python后端版）

**项目名称：** 好服务（GoodServices）社区服务撮合平台
**文档版本：** v2.0 (Python Backend)
**编制日期：** 2025-11-17
**课程：** Web开发技术 (3132111080)

---

## 目录
1. [需求分析](#一需求分析)
2. [技术栈选型](#二技术栈选型)
3. [系统架构设计](#三系统架构设计)
4. [模块拆分与设计](#四模块拆分与设计)
5. [数据库优化方案](#五数据库优化方案)
6. [关键技术方案](#六关键技术方案)
7. [开发计划与分工](#七开发计划与分工)
8. [风险评估与应对](#八风险评估与应对)

---

## 一、需求分析

### 1.1 功能需求总览

#### 1.1.1 用户角色
- **普通用户**：服务需求发布者 + 服务提供者（双重角色）
- **管理员**：系统管理、数据统计分析

#### 1.1.2 核心功能模块（按优先级）

| 优先级 | 模块名称 | 功能描述 | 复杂度 |
|--------|---------|---------|--------|
| P0（必选） | 用户注册/登录 | 用户注册、登录验证、密码校验 | 低 |
| P0（必选） | 用户信息管理 | 修改手机号、密码、用户简介 | 低 |
| P0（必选） | "我需要"模块 | 发布需求、查询、修改、删除（CRUD + 分页） | 中 |
| P0（必选） | "我服务"模块 | 响应需求、查询、修改、删除（CRUD + 分页） | 中 |
| P0（必选） | 服务撮合 | 查看响应、接受/拒绝响应、服务达成 | 中 |
| P0（必选） | 统计分析 | 按时间/地域/类型统计，图表展示 | 高 |
| P1（选作） | 管理员功能 | 查询所有用户、需求、响应信息 | 低 |
| P2（扩展） | 文件上传 | 图片、视频上传与展示 | 中 |

#### 1.1.3 关键需求约束

**密码规则：**
- 不少于6位
- 必须包含至少两个数字
- 不能全为大写或全为小写

**分页要求：**
- "我需要"查询需要分页
- "我服务"查询需要分页
- 默认每页10-20条

**数据可视化要求（必选）：**
- 按时间段（起始年月-终止年月）统计
- 按地域（省-市）筛选
- 按服务类型统计
- 图表展示：折线图/柱状图展示趋势
- 表格展示：明细数据列表
- 默认显示近6个月统计结果

---

## 二、技术栈选型

### 2.1 技术选型原则

1. **满足课程要求**：至少1种前端框架 + 2种后台框架（含数据持久化）
2. **团队技术栈**：团队成员熟悉Python，选择Python生态
3. **成熟稳定**：选择主流、社区活跃的技术栈
4. **学习成本适中**：便于团队快速上手
5. **现代化设计**：符合RESTful API规范，支持异步

### 2.2 推荐技术栈（Python全栈）

#### 2.2.1 前端技术栈

| 技术 | 版本 | 作用 | 选型理由 |
|------|------|------|---------|
| **Vue 3** | 3.3+ | 前端MVVM框架 | 渐进式框架，学习曲线平缓，中文文档完善 |
| **Element Plus** | 2.4+ | UI组件库 | 基于Vue 3，组件丰富，企业级设计 |
| **Vue Router** | 4.x | 路由管理 | Vue官方路由，支持SPA |
| **Pinia** | 2.x | 状态管理 | Vue 3推荐的状态管理库 |
| **Axios** | 1.x | HTTP客户端 | 主流的Ajax库，支持拦截器 |
| **ECharts** | 5.x | 数据可视化 | 百度开源，图表丰富，满足统计需求 |
| **Vite** | 4.x | 构建工具 | 快速的开发服务器，优秀的构建性能 |

**前端目录结构：**
```
frontend/
├── public/              # 静态资源
├── src/
│   ├── assets/         # 资源文件（图片、样式等）
│   ├── components/     # 公共组件
│   ├── views/          # 页面视图
│   │   ├── auth/      # 登录注册
│   │   ├── user/      # 用户管理
│   │   ├── service/   # 服务模块
│   │   ├── need/      # "我需要"模块
│   │   ├── response/  # "我服务"模块
│   │   └── stats/     # 统计分析
│   ├── router/        # 路由配置
│   ├── store/         # 状态管理
│   ├── api/           # API接口
│   ├── utils/         # 工具函数
│   ├── App.vue
│   └── main.js
├── package.json
└── vite.config.js
```

---

#### 2.2.2 后端技术栈 ⭐核心变化

| 技术 | 版本 | 作用 | 选型理由 |
|------|------|------|---------|
| **FastAPI** | 0.104+ | Web框架 | 现代化、高性能、自动生成API文档、异步支持 |
| **SQLAlchemy** | 2.0+ | ORM框架 | Python最流行的ORM，满足课程持久化要求 |
| **Pydantic** | 2.x | 数据验证 | FastAPI内置，类型提示，自动校验 |
| **Alembic** | 1.x | 数据库迁移 | SQLAlchemy官方迁移工具 |
| **PyJWT** | 2.x | JWT认证 | 轻量级JWT实现 |
| **Passlib** | 1.7.x | 密码加密 | 支持BCrypt等多种加密算法 |
| **PyMySQL** | 1.x | MySQL驱动 | 纯Python实现的MySQL驱动 |
| **python-multipart** | 0.0.6+ | 文件上传 | FastAPI文件上传支持 |
| **uvicorn** | 0.24+ | ASGI服务器 | 高性能异步服务器 |
| **python-jose** | 3.3+ | JWT工具 | JWT编解码 |

**满足课程要求：**
✅ **前端框架1种**：Vue 3
✅ **后台框架2种**：FastAPI（Web框架） + SQLAlchemy（ORM数据持久化框架）

---

**后端目录结构（推荐）：**
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── dependencies.py      # 依赖注入（JWT验证等）
│   │
│   ├── models/              # SQLAlchemy模型层
│   │   ├── __init__.py
│   │   ├── user.py         # 用户模型
│   │   ├── service_request.py
│   │   ├── service_response.py
│   │   └── ...
│   │
│   ├── schemas/             # Pydantic Schema层（DTO/VO）
│   │   ├── __init__.py
│   │   ├── user.py         # 用户Schema
│   │   ├── auth.py         # 认证Schema
│   │   ├── service_request.py
│   │   └── ...
│   │
│   ├── crud/                # CRUD操作层（数据访问）
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── service_request.py
│   │   └── ...
│   │
│   ├── api/                 # API路由层
│   │   ├── __init__.py
│   │   ├── v1/             # API版本1
│   │   │   ├── __init__.py
│   │   │   ├── auth.py    # 认证路由
│   │   │   ├── user.py    # 用户路由
│   │   │   ├── service_request.py
│   │   │   ├── service_response.py
│   │   │   ├── match.py   # 服务撮合
│   │   │   └── stats.py   # 统计分析
│   │   └── deps.py        # 路由依赖
│   │
│   ├── core/                # 核心功能
│   │   ├── __init__.py
│   │   ├── security.py    # 密码加密、JWT
│   │   ├── config.py      # 配置类
│   │   └── exceptions.py  # 自定义异常
│   │
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── password.py    # 密码校验
│       └── pagination.py  # 分页工具
│
├── alembic/                 # 数据库迁移
│   ├── versions/
│   └── env.py
│
├── tests/                   # 测试文件
│   ├── __init__.py
│   └── test_api.py
│
├── requirements.txt         # 依赖列表
├── .env                     # 环境变量
├── .env.example            # 环境变量示例
└── README.md
```

**核心依赖（requirements.txt）：**
```txt
# Web框架
fastapi==0.104.1
uvicorn[standard]==0.24.0

# 数据库ORM
sqlalchemy==2.0.23
pymysql==1.1.0
alembic==1.12.1

# 数据验证
pydantic==2.5.0
pydantic-settings==2.1.0

# 认证授权
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# 工具库
python-dotenv==1.0.0

# 开发工具（可选）
pytest==7.4.3
httpx==0.25.2  # 测试用
```

---

#### 2.2.3 开发工具与环境

| 工具/环境 | 版本 | 说明 |
|-----------|------|------|
| **Python** | 3.9+ / 3.10+ / 3.11 | Python运行环境（推荐3.10） |
| **Node.js** | 16+ / 18+ | 前端开发环境 |
| **MySQL** | 8.0 | 数据库 |
| **IDE** | PyCharm / VS Code | 开发工具 |
| **Git** | 2.x | 版本控制 |
| **Postman** | 最新版 | API测试 |
| **虚拟环境** | venv / conda | Python虚拟环境管理 |

---

### 2.3 Python技术栈优势

#### 2.3.1 FastAPI优势

1. **高性能**：基于Starlette和Pydantic，性能接近Node.js和Go
2. **自动文档**：自动生成OpenAPI（Swagger）文档，访问 `/docs`
3. **类型提示**：利用Python 3.6+类型提示，IDE智能提示
4. **数据验证**：Pydantic自动验证请求参数，减少手动校验
5. **异步支持**：原生支持async/await，适合IO密集型应用
6. **易学易用**：语法简洁，文档完善

**示例：自动生成的Swagger文档**
```
访问 http://localhost:8000/docs
- 自动列出所有API接口
- 可在线测试接口
- 自动生成请求/响应示例
```

#### 2.3.2 SQLAlchemy优势

1. **功能强大**：支持复杂查询、关联、事务
2. **灵活性高**：支持原生SQL和ORM混用
3. **迁移工具**：Alembic支持数据库版本管理
4. **社区活跃**：Python最流行的ORM框架

---

## 三、系统架构设计

### 3.1 总体架构

采用 **前后端分离 + RESTful API** 架构：

```
┌─────────────────────────────────────────────────────────┐
│                      用户浏览器                          │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS
                     ↓
┌─────────────────────────────────────────────────────────┐
│                   前端应用 (Vue 3)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  用户模块   │  │  需求模块   │  │  统计模块   │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                    Axios HTTP Client                     │
└────────────────────┬────────────────────────────────────┘
                     │ RESTful API (JSON)
                     ↓
┌─────────────────────────────────────────────────────────┐
│                后端应用 (FastAPI)                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │              API Router Layer                     │  │
│  │  (auth, user, service_request, ...)              │  │
│  └───────────────────┬──────────────────────────────┘  │
│                      ↓                                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │              CRUD Layer                           │  │
│  │  (用户CRUD, 需求CRUD, 响应CRUD, ...)              │  │
│  └───────────────────┬──────────────────────────────┘  │
│                      ↓                                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Model Layer (SQLAlchemy)             │  │
│  │  (User, ServiceRequest, ServiceResponse, ...)    │  │
│  └───────────────────┬──────────────────────────────┘  │
└────────────────────┬─┴──────────────────────────────────┘
                     │ PyMySQL
                     ↓
┌─────────────────────────────────────────────────────────┐
│                  MySQL 8.0 数据库                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│  │ buser   │ │ sr_info │ │response │ │ accept  │      │
│  │ _table  │ │         │ │ _info   │ │ _info   │      │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘      │
└─────────────────────────────────────────────────────────┘
```

### 3.2 分层架构说明

#### 3.2.1 后端分层（Python/FastAPI）

| 层次 | 职责 | 文件位置 |
|------|------|---------|
| **API Router层** | 接收请求、参数校验、返回响应 | `app/api/v1/*.py` |
| **CRUD层** | 数据库操作、业务逻辑 | `app/crud/*.py` |
| **Model层** | 数据库表模型（ORM映射） | `app/models/*.py` |
| **Schema层** | 数据验证、序列化 | `app/schemas/*.py` |
| **Core层** | 核心功能（安全、配置） | `app/core/*.py` |
| **Utils层** | 工具函数 | `app/utils/*.py` |

**关键概念：**
- **Model（模型）**：SQLAlchemy ORM模型，映射数据库表
- **Schema（模式）**：Pydantic模型，定义API输入/输出数据结构
- **CRUD**：Create、Read、Update、Delete数据库操作

---

### 3.3 数据流转

**请求流程：**
```
用户操作 → Vue组件 → API调用 → Axios请求
    ↓
FastAPI Router接收 → Pydantic自动校验 → CRUD处理 → SQLAlchemy查询
    ↓
MySQL返回数据 → SQLAlchemy映射 → CRUD封装 → Router返回JSON
    ↓
Axios接收 → Vue组件更新 → 页面展示
```

**认证流程：**
```
1. 用户登录 → FastAPI验证 → 生成JWT Token → 返回前端
2. 前端存储Token（localStorage）
3. 后续请求携带Token（Authorization Header）
4. FastAPI依赖注入验证Token → 放行/拒绝
```

---

## 四、模块拆分与设计

### 4.1 功能模块拆分

| 模块名称 | 前端路由 | 后端路由 | 主要功能 |
|---------|---------|----------|---------|
| **认证模块** | `/auth` | `/api/v1/auth` | 注册、登录、登出 |
| **用户模块** | `/user` | `/api/v1/users` | 个人信息管理、修改密码 |
| **服务需求模块** | `/needs` | `/api/v1/service-requests` | "我需要"CRUD、分页查询 |
| **服务响应模块** | `/responses` | `/api/v1/service-responses` | "我服务"CRUD、分页查询 |
| **服务撮合模块** | `/match` | `/api/v1/match` | 接受/拒绝响应、服务达成 |
| **统计分析模块** | `/stats` | `/api/v1/stats` | 数据统计、图表展示 |
| **管理员模块** | `/admin` | `/api/v1/admin` | 用户管理、数据管理（选作） |
| **文件模块** | `/file` | `/api/v1/files` | 文件上传、下载（可选） |

---

### 4.2 详细功能设计（Python实现）

#### 4.2.1 认证模块 - 代码示例

**Model层（app/models/user.py）：**
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class BUser(Base):
    __tablename__ = "buser_table"

    id = Column(Integer, primary_key=True, index=True)
    uname = Column(String(255), unique=True, nullable=False, index=True)
    ctype = Column(String(255), nullable=False, default="身份证")
    idno = Column(String(255), unique=True, nullable=False)
    bname = Column(String(50), nullable=False)
    bpwd = Column(String(255), nullable=False)  # 存储哈希后的密码
    phoneNo = Column(String(20), unique=True, nullable=False)
    rdate = Column(DateTime, nullable=False, server_default=func.now())
    udate = Column(DateTime, onupdate=func.now())
    userlvl = Column(String(8), default="普通用户")
    desc = Column(String(255))
```

**Schema层（app/schemas/auth.py）：**
```python
from pydantic import BaseModel, Field, validator
import re

class UserRegister(BaseModel):
    uname: str = Field(..., min_length=3, max_length=20)
    ctype: str = Field(default="身份证")
    idno: str = Field(..., min_length=18, max_length=18)
    bname: str = Field(..., min_length=2, max_length=20)
    bpwd: str = Field(..., min_length=6, max_length=20)
    phoneNo: str = Field(..., regex=r"^1[3-9]\d{9}$")
    desc: str = Field(default="", max_length=255)

    @validator("bpwd")
    def validate_password(cls, v):
        """密码校验：至少6位，至少2个数字，不能全大写或全小写"""
        if len(v) < 6:
            raise ValueError("密码不能少于6位")

        # 统计数字个数
        digit_count = sum(c.isdigit() for c in v)
        if digit_count < 2:
            raise ValueError("密码必须包含至少2个数字")

        # 检查是否全大写或全小写
        if v.isupper() or v.islower():
            raise ValueError("密码不能全部为大写或小写字母")

        return v

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_info: dict

class UserInfo(BaseModel):
    id: int
    uname: str
    bname: str
    phoneNo: str
    userlvl: str
    desc: str | None

    class Config:
        from_attributes = True  # Pydantic v2
```

**CRUD层（app/crud/user.py）：**
```python
from sqlalchemy.orm import Session
from app.models.user import BUser
from app.schemas.auth import UserRegister
from app.core.security import get_password_hash, verify_password

def get_user_by_username(db: Session, username: str):
    """根据用户名查询用户"""
    return db.query(BUser).filter(BUser.uname == username).first()

def get_user_by_phone(db: Session, phone: str):
    """根据手机号查询用户"""
    return db.query(BUser).filter(BUser.phoneNo == phone).first()

def create_user(db: Session, user: UserRegister):
    """创建用户"""
    # 密码加密
    hashed_password = get_password_hash(user.bpwd)

    db_user = BUser(
        uname=user.uname,
        ctype=user.ctype,
        idno=user.idno,
        bname=user.bname,
        bpwd=hashed_password,
        phoneNo=user.phoneNo,
        userlvl="普通用户",
        desc=user.desc
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """验证用户登录"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.bpwd):
        return None
    return user
```

**API Router层（app/api/v1/auth.py）：**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import UserRegister, UserLogin, Token, UserInfo
from app.crud import user as crud_user
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=dict)
def register(user: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    db_user = crud_user.get_user_by_username(db, user.uname)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="用户名已存在"
        )

    # 检查手机号是否已存在
    db_user = crud_user.get_user_by_phone(db, user.phoneNo)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="手机号已注册"
        )

    # 创建用户
    new_user = crud_user.create_user(db, user)

    return {
        "code": 200,
        "message": "注册成功",
        "data": {"user_id": new_user.id}
    }

@router.post("/login", response_model=dict)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = crud_user.authenticate_user(
        db,
        user_login.username,
        user_login.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误"
        )

    # 生成JWT Token
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.uname}
    )

    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "token": access_token,
            "user_info": {
                "id": user.id,
                "uname": user.uname,
                "bname": user.bname,
                "phoneNo": user.phoneNo,
                "userlvl": user.userlvl
            }
        }
    }
```

**安全模块（app/core/security.py）：**
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24小时

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """密码加密"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """生成JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """解码JWT Token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

**依赖注入（app/dependencies.py）：**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import decode_access_token
from app.crud import user as crud_user

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """获取当前登录用户（JWT验证）"""
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证"
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证"
        )

    user = db.query(BUser).filter(BUser.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )

    return user
```

**使用依赖注入的受保护路由：**
```python
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models.user import BUser

router = APIRouter()

@router.get("/me")
def get_my_info(current_user: BUser = Depends(get_current_user)):
    """获取当前用户信息（需要登录）"""
    return {
        "code": 200,
        "message": "查询成功",
        "data": {
            "id": current_user.id,
            "uname": current_user.uname,
            "bname": current_user.bname,
            "phoneNo": current_user.phoneNo,
            "desc": current_user.desc
        }
    }
```

---

#### 4.2.2 分页查询实现

**分页工具（app/utils/pagination.py）：**
```python
from typing import Generic, TypeVar, List
from pydantic import BaseModel
from sqlalchemy.orm import Query

T = TypeVar('T')

class PageResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    total: int
    pages: int
    current: int
    size: int
    records: List[T]

def paginate(query: Query, page: int = 1, size: int = 10) -> dict:
    """分页查询"""
    total = query.count()
    pages = (total + size - 1) // size
    offset = (page - 1) * size
    records = query.offset(offset).limit(size).all()

    return {
        "total": total,
        "pages": pages,
        "current": page,
        "size": size,
        "records": records
    }
```

**使用示例（app/api/v1/service_request.py）：**
```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.pagination import paginate

router = APIRouter()

@router.get("/service-requests")
def list_service_requests(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    stype_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """分页查询服务需求"""
    query = db.query(ServiceRequest).filter(ServiceRequest.ps_state == 0)

    if stype_id:
        query = query.filter(ServiceRequest.stype_id == stype_id)

    query = query.order_by(ServiceRequest.ps_begindate.desc())

    result = paginate(query, page, size)

    return {
        "code": 200,
        "message": "查询成功",
        "data": result
    }
```

---

#### 4.2.3 统计分析模块实现

**统计路由（app/api/v1/stats.py）：**
```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.database import get_db
from app.models.service_request import ServiceRequest
from app.models.accept_info import AcceptInfo
from app.models.service_type import ServiceType
from app.models.city_info import CityInfo

router = APIRouter()

@router.get("/monthly")
def get_monthly_stats(
    start_month: str = Query(..., regex=r"^\d{6}$"),
    end_month: str = Query(..., regex=r"^\d{6}$"),
    city_id: int = Query(None),
    stype_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """按月度统计服务需求和响应数"""

    # 构建查询（可以直接查report表，或者实时统计）
    # 方案1：查询report表（已有汇总数据）
    from app.models.report import Report

    query = db.query(Report).filter(
        and_(
            Report.monthID >= start_month,
            Report.monthID <= end_month
        )
    )

    if city_id:
        query = query.filter(Report.cityID == str(city_id))
    if stype_id:
        query = query.filter(Report.stype_id == stype_id)

    results = query.order_by(Report.monthID).all()

    # 组装返回数据
    list_data = []
    months = []
    ps_num_data = []
    rs_num_data = []

    for record in results:
        # 获取关联信息
        service_type = db.query(ServiceType).filter(
            ServiceType.id == record.stype_id
        ).first()

        city = db.query(CityInfo).filter(
            CityInfo.cityID == int(record.cityID)
        ).first()

        month_str = f"{record.monthID[:4]}年{record.monthID[4:]}月"

        list_data.append({
            "monthID": record.monthID,
            "month": month_str,
            "stypeId": record.stype_id,
            "stypeName": service_type.typename if service_type else "",
            "cityID": record.cityID,
            "cityName": city.cityName if city else "",
            "psNum": record.ps_num,
            "rsNum": record.rs_num
        })

        months.append(month_str)
        ps_num_data.append(record.ps_num)
        rs_num_data.append(record.rs_num)

    return {
        "code": 200,
        "message": "查询成功",
        "data": {
            "list": list_data,
            "chartData": {
                "months": months,
                "psNumData": ps_num_data,
                "rsNumData": rs_num_data
            }
        }
    }
```

---

#### 4.2.4 文件上传实现

**文件上传路由（app/api/v1/files.py）：**
```python
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "mp4", "avi"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """文件上传"""
    # 检查文件扩展名
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型，只支持: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # 读取文件内容
    contents = await file.read()

    # 检查文件大小
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="文件大小超过限制（10MB）"
        )

    # 生成唯一文件名
    file_uuid = str(uuid.uuid4())
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{date_str}_{file_uuid}.{file_ext}"
    file_path = UPLOAD_DIR / filename

    # 保存文件
    with open(file_path, "wb") as f:
        f.write(contents)

    return {
        "code": 200,
        "message": "上传成功",
        "data": {
            "filename": filename,
            "url": f"/api/v1/files/{filename}"
        }
    }

@router.get("/{filename}")
async def download_file(filename: str):
    """文件下载"""
    from fastapi.responses import FileResponse

    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")

    return FileResponse(file_path)
```

---

## 五、数据库优化方案

### 5.1 现有数据库问题

基于 `goodservices.sql` 和文档分析，发现以下问题：

| 问题 | 影响 | 优先级 |
|------|------|--------|
| report表主键只有monthID | 多条相同月份记录冲突 | 高 |
| 缺少唯一约束（uname, phoneNo, idno） | 数据重复 | 高 |
| 密码明文存储 | 安全风险 | 高 |
| 证件号明文存储 | 隐私风险 | 中 |
| response_info.desc字段类型为tinyint | 类型错误，应为varchar | 高 |

### 5.2 数据库优化SQL

**创建优化脚本 `db_optimization.sql`：**

```sql
-- 1. 修复 report 表主键（复合主键）
ALTER TABLE report DROP PRIMARY KEY;
ALTER TABLE report ADD PRIMARY KEY (monthID, stype_id, cityID);

-- 2. 添加唯一约束
ALTER TABLE buser_table ADD UNIQUE KEY uk_uname (uname);
ALTER TABLE buser_table ADD UNIQUE KEY uk_phoneNo (phoneNo);
ALTER TABLE buser_table ADD UNIQUE KEY uk_idno (idno);

-- 3. 修改 response_info.desc 字段类型
ALTER TABLE response_info MODIFY COLUMN `desc` VARCHAR(500) NOT NULL COMMENT '服务响应描述';

-- 4. 修改 buser_table.bpwd 字段长度（存储BCrypt哈希需要60字符）
ALTER TABLE buser_table MODIFY COLUMN bpwd VARCHAR(255) NOT NULL COMMENT '密码（BCrypt哈希）';

-- 5. 添加索引优化查询
CREATE INDEX idx_sr_state ON sr_info(ps_state, ps_begindate);
CREATE INDEX idx_sr_city_type ON sr_info(cityID, stype_id);
CREATE INDEX idx_response_state ON response_info(response_state, response_date);
CREATE INDEX idx_response_sr ON response_info(sr_id);
CREATE INDEX idx_accept_date ON accept_info(createdate);

-- 6. 添加状态检查约束（MySQL 8.0.16+）
ALTER TABLE sr_info ADD CONSTRAINT chk_sr_state CHECK (ps_state IN (0, -1));
ALTER TABLE response_info ADD CONSTRAINT chk_response_state CHECK (response_state IN (0, 1, 2, 3));
```

### 5.3 使用Alembic管理数据库迁移

**初始化Alembic：**
```bash
# 安装alembic
pip install alembic

# 初始化
alembic init alembic

# 配置 alembic.ini（修改数据库连接）
sqlalchemy.url = mysql+pymysql://root:password@localhost:3306/goodservices

# 生成迁移脚本
alembic revision -m "initial migration"

# 执行迁移
alembic upgrade head
```

---

## 六、关键技术方案

### 6.1 项目配置管理

**配置文件（app/core/config.py）：**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "GoodServices"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/goodservices"

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024

    class Config:
        env_file = ".env"

settings = Settings()
```

**环境变量文件（.env）：**
```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/goodservices
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
```

---

### 6.2 数据库连接管理

**数据库配置（app/database.py）：**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 连接池预检查
    echo=settings.DEBUG  # 开发模式打印SQL
)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 模型基类
Base = declarative_base()

# 依赖注入：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### 6.3 FastAPI应用入口

**主应用（app/main.py）：**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, user, service_request, service_response, match, stats

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",  # Swagger文档
    redoc_url="/redoc"  # ReDoc文档
)

# CORS配置（允许前端跨域请求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vue开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(user.router, prefix="/api/v1/users", tags=["用户"])
app.include_router(service_request.router, prefix="/api/v1/service-requests", tags=["服务需求"])
app.include_router(service_response.router, prefix="/api/v1/service-responses", tags=["服务响应"])
app.include_router(match.router, prefix="/api/v1/match", tags=["服务撮合"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["统计分析"])

@app.get("/")
def read_root():
    return {"message": "GoodServices API", "version": settings.APP_VERSION}

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

**启动应用：**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问：
- API接口：http://localhost:8000
- Swagger文档：http://localhost:8000/docs
- ReDoc文档：http://localhost:8000/redoc

---

## 七、开发计划与分工

### 7.1 开发阶段划分

按照教学周（15-17周）制定开发计划：

| 阶段 | 时间 | 任务 | 产出 |
|------|------|------|------|
| **第一阶段** | 第15周 | 环境搭建、基础架构 | 项目框架、数据库优化 |
| **第二阶段** | 第16周 | 核心功能开发 | 用户、需求、响应模块 |
| **第三阶段** | 第17周 | 统计分析、测试、文档 | 完整系统、报告 |

---

### 7.2 详细任务分解（第15周）

**环境搭建与基础架构（3-4天）**

#### 任务1：项目初始化（1人，1天）
- [ ] 安装Python 3.10+、Node.js
- [ ] 创建虚拟环境：`python -m venv venv`
- [ ] 创建前端项目：`npm create vite@latest frontend -- --template vue`
- [ ] 创建后端项目目录结构
- [ ] 安装后端依赖：`pip install -r requirements.txt`
- [ ] 配置Git仓库

#### 任务2：数据库优化（1人，1天）
- [ ] 执行数据库优化脚本 `db_optimization.sql`
- [ ] 导入测试数据 `test_data.sql`
- [ ] 验证数据完整性
- [ ] 配置数据库连接（.env文件）

#### 任务3：后端基础架构（1人，2天）
- [ ] 配置FastAPI应用（main.py）
- [ ] 配置数据库连接（database.py）
- [ ] 创建SQLAlchemy模型（models/）
- [ ] 配置JWT认证（core/security.py）
- [ ] 创建依赖注入（dependencies.py）
- [ ] 测试Swagger文档（/docs）

#### 任务4：前端基础架构（1人，1天）
- [ ] 配置Vue Router
- [ ] 配置Pinia Store
- [ ] 配置Axios拦截器
- [ ] 封装API接口
- [ ] 设计主布局（Layout）
- [ ] 安装Element Plus

**里程碑1：** 项目框架搭建完成，FastAPI能运行，Swagger文档可访问

---

### 7.3 详细任务分解（第16周）

**核心功能开发（5-6天）**

#### 任务5：认证模块（1人，2天）
- [ ] 后端：用户Model + Schema
- [ ] 后端：注册接口（含密码校验）
- [ ] 后端：登录接口（JWT生成）
- [ ] 后端：JWT依赖注入
- [ ] 前端：注册页面
- [ ] 前端：登录页面
- [ ] 前端：Token存储与拦截器

#### 任务6：用户模块（1人，1天）
- [ ] 后端：获取/修改用户信息接口
- [ ] 后端：修改密码接口
- [ ] 前端：个人中心页面
- [ ] 前端：修改密码页面

#### 任务7："我需要"模块（1人，2天）
- [ ] 后端：ServiceRequest Model
- [ ] 后端：CRUD接口 + 分页
- [ ] 前端：需求列表页面（分页）
- [ ] 前端：发布需求页面
- [ ] 前端：需求详情页面

#### 任务8："我服务"模块（1人，2天）
- [ ] 后端：ServiceResponse Model
- [ ] 后端：CRUD接口 + 分页
- [ ] 前端：响应列表页面（分页）
- [ ] 前端：提交响应页面

#### 任务9：服务撮合模块（1人，1天）
- [ ] 后端：接受/拒绝响应接口（事务）
- [ ] 后端：服务达成记录接口
- [ ] 前端：响应确认对话框
- [ ] 前端：服务达成记录页面

**里程碑2：** 核心业务功能完成，能完成服务撮合流程

---

### 7.4 详细任务分解（第17周）

**统计分析、测试、文档（5-6天）**

#### 任务10：统计分析模块（2人，3天）⭐必选
- [ ] 后端：月度统计查询接口
- [ ] 前端：统计分析页面
- [ ] 前端：查询条件表单
- [ ] 前端：ECharts折线图展示
- [ ] 前端：数据明细表格
- [ ] 前端：图表交互优化

#### 任务11：文件上传模块（1人，1天）（可选）
- [ ] 后端：文件上传接口
- [ ] 后端：文件下载接口
- [ ] 前端：文件上传组件
- [ ] 前端：图片预览功能

#### 任务12：测试与修复（全员，2天）
- [ ] 功能测试（Postman测试所有接口）
- [ ] 界面测试（Chrome、Firefox）
- [ ] 性能测试（分页、查询）
- [ ] Bug修复
- [ ] 代码优化

#### 任务13：文档编写（1人，2天）
- [ ] 运行环境配置说明
- [ ] 已实现功能清单
- [ ] 关键界面截图
- [ ] API接口文档（Swagger导出）
- [ ] 小组分工说明
- [ ] 导出数据库SQL（mysqldump）
- [ ] 打包提交文件

**里程碑3：** 项目完成，通过验收

---

### 7.5 团队分工建议（3人小组）

#### 角色1：后端开发+项目负责人
**职责：**
- 后端框架搭建
- 数据库模型设计
- 认证模块开发
- 统计分析模块开发（后端）
- 技术难点攻关
- 代码审查

**工作量占比：** 40%

#### 角色2：后端开发
**职责：**
- 数据库优化
- "我需要"模块开发（后端）
- "我服务"模块开发（后端）
- 服务撮合模块开发（后端）
- 文件上传模块

**工作量占比：** 30%

#### 角色3：前端开发+测试
**职责：**
- 前端基础架构
- 所有页面开发
- 统计分析模块开发（前端+ECharts）
- 功能测试
- 文档编写

**工作量占比：** 30%

---

### 7.6 开发规范

#### 7.6.1 Python代码规范（PEP 8）

**命名规范：**
- 类名：大驼峰（`UserService`）
- 函数名：小写下划线（`get_user_info`）
- 常量：全大写下划线（`MAX_FILE_SIZE`）
- 变量：小写下划线（`user_name`）

**注释规范：**
```python
def create_user(db: Session, user: UserRegister) -> BUser:
    """
    创建新用户

    Args:
        db: 数据库会话
        user: 用户注册信息

    Returns:
        创建的用户对象

    Raises:
        ValueError: 当用户名已存在时
    """
    pass
```

**类型提示：**
```python
def get_user_by_id(db: Session, user_id: int) -> Optional[BUser]:
    return db.query(BUser).filter(BUser.id == user_id).first()
```

#### 7.6.2 Git规范

**分支策略：**
- `main`：主分支，稳定版本
- `dev`：开发分支
- `feature/xxx`：功能分支
- `bugfix/xxx`：修复分支

**提交信息规范：**
```
feat: 添加用户登录功能
fix: 修复分页查询bug
docs: 更新README文档
style: 代码格式化
refactor: 重构统计查询逻辑
test: 添加单元测试
chore: 更新依赖版本
```

---

## 八、风险评估与应对

### 8.1 技术风险

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|---------|
| SQLAlchemy ORM学习曲线 | 中 | 中 | 提前学习官方文档，参考示例代码 |
| FastAPI依赖注入理解难 | 中 | 中 | 学习官方教程，理解Depends机制 |
| 异步编程概念混乱 | 低 | 低 | 初期使用同步代码，后期优化 |
| Pydantic数据验证复杂 | 低 | 低 | 使用装饰器和内置验证器 |
| JWT实现细节多 | 中 | 中 | 使用成熟库python-jose |

### 8.2 时间风险

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|---------|
| 需求理解偏差 | 高 | 中 | 提前与老师确认需求 |
| 开发进度延误 | 高 | 中 | 每周进度检查，及时调整 |
| Python环境配置问题 | 中 | 低 | 使用虚拟环境，统一版本 |
| 临近验收bug多 | 高 | 中 | 提前2周完成开发，预留测试时间 |

### 8.3 团队风险

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|---------|
| Python水平不均 | 中 | 中 | 经验分享会，代码审查 |
| 沟通不畅 | 中 | 中 | 建立微信群，每日站会 |
| 分工不明确 | 高 | 低 | 明确任务清单，责任到人 |

---

## 九、总结

### 9.1 技术栈总结

**前端：** Vue 3 + Element Plus + ECharts + Axios
**后端：** FastAPI + SQLAlchemy + Pydantic + JWT
**数据库：** MySQL 8.0

✅ **满足课程要求：**
- 1种前端框架：Vue 3
- 2种后台框架：FastAPI（Web框架） + SQLAlchemy（ORM数据持久化框架）

### 9.2 Python技术栈优势

1. **开发效率高**：Python语法简洁，FastAPI开发速度快
2. **自动文档生成**：Swagger/OpenAPI自动生成，无需手写
3. **类型安全**：Pydantic自动验证，减少bug
4. **团队熟悉**：团队成员熟悉Python，学习成本低
5. **生态丰富**：大量第三方库，问题容易解决

### 9.3 核心优势

1. **技术栈现代化**：FastAPI是近年最火的Python Web框架
2. **架构清晰合理**：前后端分离，RESTful API，分层设计
3. **开发体验好**：自动重载、类型提示、自动文档
4. **文档完善详细**：Swagger文档、开发文档、数据库文档
5. **开发计划可行**：3周时间，任务分解细致，风险可控

### 9.4 关键成功因素

1. ✅ **第15周完成环境搭建**（Python虚拟环境、FastAPI运行）
2. ✅ **第16周完成核心模块**（用户、需求、响应）
3. ✅ **第17周完成统计分析**（必选项，图表展示）
4. ✅ **预留充足测试时间**（至少2天）
5. ✅ **提前准备演示材料**

### 9.5 验收准备清单

- [ ] 源代码工程（frontend/ + backend/）
- [ ] requirements.txt（Python依赖）
- [ ] package.json（前端依赖）
- [ ] 数据库SQL文件（goodservices.sql + 优化脚本 + 测试数据）
- [ ] 设计与实现说明报告（含截图、架构图）
- [ ] 小组分工说明（每人贡献百分比）
- [ ] 演示笔记本（部署好程序）
- [ ] 演示流程（注册→登录→发布需求→响应→统计）

---

**文档版本：** v2.0 (Python Backend)
**编制日期：** 2025-11-17
**最后更新：** 2025-11-17
**编制人：** Claude Code

---

## 附录A：快速启动命令

### 环境安装

**安装Python依赖：**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**安装前端依赖：**
```bash
cd frontend
npm install
```

### 数据库初始化

```bash
# 登录MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE goodservices CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 导入数据
mysql -u root -p goodservices < goodservices.sql
mysql -u root -p goodservices < db_optimization.sql
mysql -u root -p goodservices < test_data.sql
```

### 启动服务

**启动后端：**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 访问：
# API: http://localhost:8000
# Swagger文档: http://localhost:8000/docs
```

**启动前端：**
```bash
cd frontend
npm run dev

# 访问: http://localhost:3000
```

---

## 附录B：参考资料

### Python后端
- **FastAPI官方文档：** https://fastapi.tiangolo.com/zh/
- **SQLAlchemy文档：** https://docs.sqlalchemy.org/
- **Pydantic文档：** https://docs.pydantic.dev/
- **python-jose文档：** https://python-jose.readthedocs.io/

### 前端
- **Vue 3官方文档：** https://cn.vuejs.org/
- **Element Plus文档：** https://element-plus.org/zh-CN/
- **ECharts文档：** https://echarts.apache.org/zh/index.html

### 学习资源
- **FastAPI教程（中文）：** https://fastapi.tiangolo.com/zh/tutorial/
- **SQLAlchemy教程：** https://docs.sqlalchemy.org/en/20/tutorial/

---

## 附录C：常见问题解决

### 1. MySQL连接问题

**问题：** `pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")`

**解决：**
```bash
# 检查MySQL服务是否启动
sudo service mysql status

# 启动MySQL
sudo service mysql start

# 检查端口
netstat -an | grep 3306
```

### 2. Python依赖安装失败

**问题：** `error: Microsoft Visual C++ 14.0 is required`

**解决：**
```bash
# Windows: 安装Visual C++ Build Tools
# Linux: 安装python-dev
sudo apt install python3-dev

# macOS: 安装Xcode Command Line Tools
xcode-select --install
```

### 3. FastAPI自动重载不工作

**问题：** 修改代码后不自动重载

**解决：**
```bash
# 确保使用 --reload 参数
uvicorn app.main:app --reload

# 或使用 watchfiles
pip install watchfiles
uvicorn app.main:app --reload --reload-delay 1
```

---

**祝Python开发顺利！🐍🎉**
