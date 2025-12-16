# GoodServices 数据库

本目录包含 GoodServices 项目的所有数据库相关文件。

## 文件说明

### schema/goodservices.sql
主数据库架构定义文件，包含所有数据库表的 DDL（数据定义语言）。

**包含的表:**
- `buser_table` - 业务用户表（核心用户信息）
- `auser_table` - 管理员用户表
- `sr_info` - 服务请求表（"我需要"模块）
- `response_info` - 服务响应表（"我服务"模块）
- `accept_info` - 服务接受/完成表（服务匹配）
- `service_type` - 服务类型表（6 种固定类型）
- `city_info` - 城市信息表
- `report` - 月度统计报告表（统计模块）

**使用方式:**
```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE goodservices;"

# 导入架构
mysql -u root -p goodservices < database/schema/goodservices.sql
```

### schema/db_optimization.sql
数据库优化脚本，包含索引、主键修复等优化操作。

**包含的优化:**
- 为高频查询列添加索引
- 修复 `report` 表的复合主键设计
- 调整字段长度以支持 BCrypt 密码哈希（255 字符）
- 添加外键约束

**使用方式:**
```bash
# 在导入主架构后应用优化
mysql -u root -p goodservices < database/schema/db_optimization.sql
```

**注意:** 优化脚本应该在主架构之后运行，不应该替代主架构。

### schema/test_data.sql
测试数据初始化脚本，包含用于开发和测试的示例数据。

**包含的数据:**
- 测试用户账户
- 示例服务请求
- 示例服务响应
- 示例服务接受记录
- 示例统计数据

**使用方式:**
```bash
# （可选）导入测试数据用于开发
mysql -u root -p goodservices < database/schema/test_data.sql
```

**注意:** 该文件仅用于开发和测试，生产环境不应导入。

## 数据库初始化步骤

### 方式 1：使用 Docker Compose（推荐）

```bash
# docker-compose.yml 会自动执行以下步骤：
# 1. 创建 MySQL 容器
# 2. 导入 goodservices.sql
# 3. 应用优化

docker-compose -f config/docker-compose.yml up -d mysql
```

Docker Compose 配置会自动将 SQL 文件挂载为初始化脚本，数据库启动时自动执行。

### 方式 2：手动导入

```bash
# 1. 启动 MySQL
mysql -u root -p

# 2. 创建数据库
CREATE DATABASE goodservices CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 3. 导入主架构（退出 MySQL 后）
mysql -u root -p goodservices < database/schema/goodservices.sql

# 4. 应用优化
mysql -u root -p goodservices < database/schema/db_optimization.sql

# 5. （可选）导入测试数据
mysql -u root -p goodservices < database/schema/test_data.sql

# 6. 验证导入
mysql -u root -p -e "USE goodservices; SHOW TABLES;"
```

## 数据库架构概览

### 用户相关表

#### buser_table（业务用户）
- `userid`: 用户 ID（主键）
- `uname`: 用户名（唯一）
- `bpwd`: 密码（BCrypt 哈希，255 字符）
- `phoneNo`: 电话号码（唯一）
- `cityid`: 城市 ID
- `idno`: 身份证号
- `createdate`: 创建时间

#### auser_table（管理员用户）
- `adid`: 管理员 ID
- `username`: 管理员用户名
- `password`: 密码
- `createdate`: 创建时间

### 服务相关表

#### sr_info（服务请求）
- `srid`: 服务请求 ID（主键）
- `psr_userid`: 发起者用户 ID（外键）
- `stype_id`: 服务类型 ID（外键）
- `cityid`: 城市 ID（外键）
- `ps_title`: 请求标题
- `ps_content`: 请求内容
- `ps_state`: 请求状态（0=发布, -1=取消）
- `createdate`: 创建时间
- `file_list`: 附件文件列表（逗号分隔）

#### response_info（服务响应）
- `response_id`: 响应 ID（主键）
- `srid`: 服务请求 ID（外键）
- `response_userid`: 响应者用户 ID（外键）
- `response_state`: 响应状态（0=待处理, 1=已接受, 2=已拒绝, 3=已取消）
- `response_content`: 响应内容
- `createdate`: 创建时间
- `response_price`: 响应价格
- `file_list`: 附件文件列表

#### accept_info（服务接受/完成）
- `accept_id`: 接受 ID（主键）
- `response_id`: 响应 ID（外键）
- `accept_description`: 接受描述
- `createdate`: 服务完成时间

### 分类表

#### service_type（服务类型）
6 种固定的服务类型：
1. 水管维修 (Plumbing)
2. 老人护理 (Elderly Care)
3. 保洁服务 (Cleaning)
4. 医疗服务 (Medical)
5. 餐食配送 (Meals)
6. 交通服务 (Transportation)

#### city_info（城市信息）
存储服务覆盖的城市列表。

### 统计表

#### report（月度统计）
- `monthID`: 年月（格式: YYYYMM）
- `stype_id`: 服务类型 ID（组合主键）
- `cityID`: 城市 ID（组合主键）
- `count`: 该月该类型该城市的服务数量
- `flag`: 统计标记

**注意:** 主键已修复为组合主键 `(monthID, stype_id, cityID)` 以避免重复。

## 关键字段说明

### 密码字段
- 字段：`bpwd`（buser_table）、`password`（auser_table）
- 长度：255 字符（支持 BCrypt 哈希）
- 存储：应该存储 BCrypt 哈希值，不应该存储明文

### 状态字段

**ps_state（服务请求状态）:**
- `0`: 已发布
- `-1`: 已取消

**response_state（服务响应状态）:**
- `0`: 待处理
- `1`: 已接受
- `2`: 已拒绝
- `3`: 已取消

## 备份和恢复

### 备份数据库

```bash
# 完整备份（包含数据和结构）
mysqldump -u root -p goodservices > backup.sql

# 仅备份结构
mysqldump -u root -p --no-data goodservices > schema_backup.sql

# 压缩备份
mysqldump -u root -p goodservices | gzip > backup.sql.gz
```

### 恢复数据库

```bash
# 从备份恢复
mysql -u root -p goodservices < backup.sql

# 从压缩备份恢复
gunzip < backup.sql.gz | mysql -u root -p goodservices
```

## 性能优化

### 已应用的索引

主要索引包括：
- 用户名和电话号码（唯一索引）
- 服务请求的发起者用户 ID
- 服务响应的服务请求 ID 和响应用户 ID
- 统计表的时间和类型字段

### 查询优化建议

1. **用户查询**：使用 `userid` 或 `uname`
2. **服务请求查询**：按 `psr_userid` 或 `stype_id` 过滤
3. **响应查询**：按 `srid` 查找特定请求的响应
4. **统计查询**：按 `monthID` 和 `stype_id` 聚合

## 常见问题

### Q: 如何添加新用户？
A: 使用 `buser_table` 的 INSERT 语句，确保：
- `uname` 唯一
- `phoneNo` 唯一
- `bpwd` 是 BCrypt 哈希值

### Q: 如何导出用于提交的 SQL？
A:
```bash
# 导出整个数据库（包含数据）
mysqldump -u root -p goodservices > final_goodservices.sql

# 导出供课程提交
cp final_goodservices.sql ../sql.txt
```

### Q: 数据库密码安全吗？
A: 当前架构：
- ✓ 密码字段长度支持 BCrypt 哈希
- ✓ 建议使用 BCrypt 或 Argon2 进行密码哈希
- ⚠ 身份证号未加密（应考虑加密存储）

### Q: 如何处理 CORS 跨域问题？
A: CORS 在应用层处理，不在数据库层。详见 `docs/TECHNICAL_SOLUTION.md`。

## 相关文档

- [../docs/DATABASE_DOCUMENTATION.md](../docs/DATABASE_DOCUMENTATION.md) - 详细数据库文档
- [../docs/TECHNICAL_SOLUTION.md](../docs/TECHNICAL_SOLUTION.md) - 技术方案
- [../backend/README.md](../backend/README.md) - 后端说明

## 维护

### 定期备份
建议每次重要更新后都执行备份：
```bash
mysqldump -u root -p goodservices > backups/backup_$(date +%Y%m%d_%H%M%S).sql
```

### 监控数据库大小
```bash
SELECT table_name, ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = 'goodservices';
```

---

**最后更新**: 2025-12-16
