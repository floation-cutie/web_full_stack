# GoodServices Database Schema Management Guide

## SQL 文件说明

本项目包含多个 SQL 文件，每个文件有不同的用途和执行时机。

---

## 文件清单

### 1. `goodservices.sql` - 基础 Schema
**用途：** 数据库初始结构定义  
**内容：**
- 所有表的 CREATE TABLE 语句
- 表结构定义（字段、类型、注释）
- 外键关系定义
- 基础索引定义
- 初始数据（service_type, auser_table 等）

**执行时机：**
- ✅ Docker 首次启动时自动执行
- ✅ 数据库重建时执行
- ❌ 不要在运行中的数据库手动执行（会报错）

**挂载配置：**
```yaml
- ./goodservices.sql:/docker-entrypoint-initdb.d/01-schema.sql
```

**何时修改：**
- 新增表
- 修改表结构（字段类型、长度等）
- 添加/删除字段
- 修改外键关系

**注意事项：**
⚠️ 修改此文件后需要**重建数据库**才能生效：
```bash
docker-compose down -v  # 删除数据卷（会丢失所有数据！）
docker-compose up -d    # 重新创建
```

---

### 2. `db_optimization.sql` - 数据库优化脚本
**用途：** 对已有 schema 的优化和修正  
**内容：**
- ALTER TABLE 语句（修改表结构）
- 添加索引（提升性能）
- 添加约束（数据完整性）
- 修复设计问题

**执行时机：**
- ✅ Docker 首次启动时，在 01-schema.sql 之后自动执行
- ✅ 数据库重建时执行
- ✅ 可在运行中的数据库手动执行（作为迁移脚本）

**挂载配置：**
```yaml
- ./db_optimization.sql:/docker-entrypoint-initdb.d/02-optimization.sql
```

**何时修改：**
- 添加新的性能优化索引
- 修复已有表的问题（如字段长度不足）
- 添加新的约束条件
- 数据库版本升级

**手动执行（运行中数据库）：**
```bash
docker exec -i goodservices-mysql mysql -uroot -prootpassword123 goodservices < db_optimization.sql
```

---

## SQL 文件执行顺序

Docker MySQL 容器初始化时按文件名**字母顺序**执行：

```
/docker-entrypoint-initdb.d/
├── 01-schema.sql          (goodservices.sql)    ← 先执行
└── 02-optimization.sql    (db_optimization.sql) ← 后执行
```

**为什么这样设计？**
1. **01-schema.sql** 创建表结构
2. **02-optimization.sql** 在已有结构上优化

如果顺序反了，ALTER TABLE 会失败（表不存在）。

---

## 使用场景对比

### 场景 1: 全新部署（首次启动）
```bash
./deploy.sh dev
```
- ✅ 自动执行 01-schema.sql
- ✅ 自动执行 02-optimization.sql
- ✅ 数据库完全就绪

### 场景 2: 数据库已存在，修改了 goodservices.sql
```bash
# 选项A: 重建数据库（会丢失所有数据）
docker-compose down -v
docker-compose up -d

# 选项B: 手动执行 ALTER TABLE 语句（推荐）
# 将修改提取为单独的迁移脚本
```

### 场景 3: 数据库已存在，只修改了 db_optimization.sql
```bash
# 新增的优化可以直接执行
docker exec -i goodservices-mysql mysql -uroot -prootpassword123 goodservices < db_optimization.sql
```

### 场景 4: 数据库已存在，需要应用某个新的迁移
```bash
# 创建迁移脚本
cat > migration_xxx.sql << 'SQL'
ALTER TABLE some_table ADD COLUMN new_field VARCHAR(50);
SQL

# 执行迁移
docker exec -i goodservices-mysql mysql -uroot -prootpassword123 goodservices < migration_xxx.sql
```

---

## 最佳实践

### ✅ DO (推荐做法)

1. **修改基础结构 → 更新 goodservices.sql**
   - 新增表、修改字段类型、外键关系
   - 在开发环境重建数据库测试
   - 生产环境使用迁移脚本

2. **性能优化 → 更新 db_optimization.sql**
   - 添加索引
   - 添加约束
   - 可以安全地在运行中数据库执行

3. **生产环境升级 → 创建独立迁移脚本**
   - 每次 schema 变更创建新的 migration_YYYYMMDD_description.sql
   - 保留历史迁移记录
   - 顺序执行迁移

### ❌ DON'T (避免)

1. ❌ 不要在生产环境直接 `docker-compose down -v`（会丢失数据）
2. ❌ 不要在运行中数据库执行 goodservices.sql（会报错）
3. ❌ 不要混合修改两个文件导致冲突
4. ❌ 不要跳过备份直接修改数据库

---

## 当前项目状态

### 已配置的 SQL 文件

| 文件 | 挂载路径 | 执行顺序 | 状态 |
|------|---------|---------|------|
| goodservices.sql | /docker-entrypoint-initdb.d/01-schema.sql | 1 | ✅ 已挂载 |
| db_optimization.sql | /docker-entrypoint-initdb.d/02-optimization.sql | 2 | ✅ 已挂载 |

### 关键修复（已包含在 db_optimization.sql）

- ✅ bpwd 字段扩展到 VARCHAR(255)（支持 BCrypt）
- ✅ 添加唯一约束（uname, phoneNo, idno）
- ✅ 修复 report 表复合主键
- ✅ 添加 5 个性能索引
- ✅ 修正 response_info.desc 类型

---

## 故障排查

### 问题：修改了 SQL 文件但没有生效
**原因：** docker-entrypoint-initdb.d 只在首次启动执行  
**解决：** 
```bash
# 查看数据库当前状态
docker exec goodservices-mysql mysql -uroot -prootpassword123 -e "DESCRIBE goodservices.buser_table;"

# 选项1: 重建（开发环境）
docker-compose down -v && docker-compose up -d

# 选项2: 手动执行（生产环境）
docker exec -i goodservices-mysql mysql -uroot -prootpassword123 goodservices < db_optimization.sql
```

### 问题：执行 ALTER TABLE 报错
**可能原因：**
- 字段已存在
- 索引名冲突
- 数据类型不兼容

**解决：** 检查当前表结构，调整 SQL 语句

---

## 参考

- [MySQL Docker 初始化文档](https://hub.docker.com/_/mysql) - Section "Initializing a fresh instance"
- 项目数据库文档：`goodservices_database_documentation.md`
