# GoodServices 数据库设置指南

**快速参考指南** - 如何应用数据库优化和导入测试数据

---

## 快速开始（5分钟）

### 步骤1：准备备份（生产环境必须）

```bash
# 备份现有数据库
mysqldump -u root -p goodservices > backup_$(date +%Y%m%d_%H%M%S).sql
echo "备份完成"
```

### 步骤2：应用优化脚本

```bash
# 方式A：使用命令行
mysql -u root -p goodservices < db_optimization.sql

# 方式B：登录MySQL后执行
mysql -u root -p
USE goodservices;
source /path/to/db_optimization.sql;
```

### 步骤3：导入测试数据

```bash
# 方式A：使用命令行
mysql -u root -p goodservices < test_data.sql

# 方式B：登录MySQL后执行
mysql -u root -p
USE goodservices;
source /path/to/test_data.sql;
```

### 步骤4：验证结果

```bash
mysql -u root -p goodservices
```

在MySQL中执行验证查询：

```sql
-- 检查主键
DESCRIBE report;
-- 应显示：monthID, stype_id, cityID 为主键

-- 检查唯一约束
SHOW KEYS FROM buser_table;
-- 应显示：uk_uname, uk_phoneNo, uk_idno

-- 检查数据
SELECT COUNT(*) as user_count FROM buser_table;
-- 应返回：5

SELECT COUNT(*) as request_count FROM sr_info;
-- 应返回：12

SELECT COUNT(*) as response_count FROM response_info;
-- 应返回：15

SELECT COUNT(*) as completed_count FROM accept_info;
-- 应返回：5

SELECT COUNT(*) as report_count FROM report;
-- 应返回：30
```

---

## 详细步骤

### 前置要求

- MySQL 8.0及以上版本
- goodservices数据库已存在
- 拥有ALTER TABLE权限
- 磁盘空间充足（至少100MB）

### 执行顺序

**重要：必须按照以下顺序执行**

1. **备份原数据库** ← 必须
2. **应用优化脚本** `db_optimization.sql` ← 修改schema
3. **导入测试数据** `test_data.sql` ← 填充数据

### 详细执行步骤

#### 步骤1：备份数据

**Windows:**
```cmd
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
mysqldump -u root -p goodservices > C:\backup\goodservices_backup.sql
```

**Linux/macOS:**
```bash
mkdir -p ~/db_backups
mysqldump -u root -p goodservices > ~/db_backups/goodservices_backup_$(date +%Y%m%d).sql
```

#### 步骤2：应用优化脚本

**方案A - 命令行执行（推荐）**

```bash
# 在包含db_optimization.sql的目录下执行
mysql -u root -p goodservices < db_optimization.sql

# 成功标志：
# ============================================
# 优化完成总结
# ============================================
```

**方案B - MySQL交互模式**

```bash
# 登录MySQL
mysql -u root -p

# 登录后执行：
USE goodservices;
SET FOREIGN_KEY_CHECKS = 0;
source db_optimization.sql;
SET FOREIGN_KEY_CHECKS = 1;
EXIT;
```

**方案C - Python脚本执行**

```python
import mysql.connector
from mysql.connector import Error

def apply_optimization():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',
            database='goodservices'
        )
        cursor = connection.cursor()

        # 读取优化脚本
        with open('db_optimization.sql', 'r', encoding='utf-8') as f:
            script = f.read()

        # 分割SQL语句并执行
        for statement in script.split(';'):
            if statement.strip():
                cursor.execute(statement)

        connection.commit()
        print("✓ 优化脚本执行成功")

    except Error as e:
        print(f"✗ 执行失败: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    apply_optimization()
```

#### 步骤3：导入测试数据

```bash
# 方法1：直接导入（推荐）
mysql -u root -p goodservices < test_data.sql

# 方法2：登录后导入
mysql -u root -p
USE goodservices;
source test_data.sql;
EXIT;

# 预期输出：
# === GoodServices 测试数据导入统计 ===
# 用户总数: 5
# 服务需求总数: 12
# 服务响应总数: 15
# 服务达成记录数: 5
# 统计记录总数: 30
# === 数据导入完成 ===
```

---

## 验证清单

### 执行完成后的验证

```sql
-- 连接到goodservices数据库
USE goodservices;

-- 1. 验证Report表主键（应为复合主键）
DESCRIBE report;
SHOW KEYS FROM report;
-- 预期：主键由 (monthID, stype_id, cityID) 组成

-- 2. 验证唯一约束
SHOW KEYS FROM buser_table WHERE Key_name LIKE 'uk_%';
-- 预期：
-- uk_uname      ✓
-- uk_phoneNo    ✓
-- uk_idno       ✓

-- 3. 验证字段长度
DESCRIBE buser_table;
-- 预期：bpwd VARCHAR(255)

DESCRIBE response_info;
-- 预期：desc VARCHAR(500)

-- 4. 验证索引创建
SHOW KEYS FROM sr_info WHERE Key_name LIKE 'idx_%';
-- 预期：
-- idx_sr_state_date
-- idx_sr_city_type

SHOW KEYS FROM response_info WHERE Key_name LIKE 'idx_%';
-- 预期：
-- idx_response_state
-- idx_response_sr

SHOW KEYS FROM accept_info WHERE Key_name LIKE 'idx_%';
-- 预期：
-- idx_accept_date

-- 5. 验证数据完整性
SELECT
    '用户' as metric, COUNT(*) as count FROM buser_table
UNION ALL
SELECT '需求', COUNT(*) FROM sr_info
UNION ALL
SELECT '响应', COUNT(*) FROM response_info
UNION ALL
SELECT '达成', COUNT(*) FROM accept_info
UNION ALL
SELECT '统计', COUNT(*) FROM report;

-- 预期：
-- 用户: 5
-- 需求: 12
-- 响应: 15
-- 达成: 5
-- 统计: 30

-- 6. 验证约束
SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.CHECK_CONSTRAINTS
WHERE TABLE_SCHEMA = 'goodservices';
-- 预期：
-- chk_sr_state
-- chk_response_state

-- 7. 测试唯一约束
-- 尝试插入重复用户名（应失败）
INSERT INTO buser_table (uname, ctype, idno, bname, bpwd, phoneNo, rdate)
VALUES ('user_zhang', '身份证', '999999999999999999', 'Test', 'test', '19999999999', NOW());
-- 预期：Error 1062 - Duplicate entry for key 'uk_uname'

-- 8. 查看约束的详细信息
SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'goodservices' AND TABLE_NAME = 'buser_table';
```

---

## 常见问题解决

### Q1：执行优化脚本时出错"Duplicate entry"

**原因：** 表中已存在重复的用户名、电话或身份证号

**解决方案：**
```sql
-- 查看重复项
SELECT uname, COUNT(*) FROM buser_table GROUP BY uname HAVING COUNT(*) > 1;

-- 删除重复记录（保留第一条）
DELETE FROM buser_table WHERE id NOT IN (
    SELECT MIN(id) FROM (
        SELECT MIN(id) FROM buser_table GROUP BY uname
    ) AS t
);

-- 重新执行优化脚本
source db_optimization.sql;
```

### Q2：MySQL版本过低，CHECK约束不支持

**错误信息：** "Syntax error near 'CHECK'"

**解决方案：**
```bash
# 检查MySQL版本
mysql --version

# 需要升级到8.0.16或以上
# 暂时可跳过CHECK约束相关行（保留其他优化）
```

### Q3：导入测试数据时外键约束冲突

**错误信息：** "Foreign key constraint fails"

**解决方案：**
```sql
-- 禁用外键检查（仅导入时使用）
SET FOREIGN_KEY_CHECKS = 0;

-- 执行导入
source test_data.sql;

-- 重新启用外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- 验证外键完整性
SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'goodservices';
```

### Q4：磁盘空间不足

**症状：** "ERROR 1030 (HY000): Got error 28 from storage engine"

**解决方案：**
```bash
# Linux/macOS
df -h /var/lib/mysql/

# Windows
# 检查MySQL数据目录的剩余空间
# 一般在 C:\ProgramData\MySQL\MySQL Server 8.0\data\

# 清理临时文件
mysql -u root -p -e "OPTIMIZE TABLE goodservices.buser_table, goodservices.sr_info;"

# 或扩展磁盘空间
```

### Q5：密码包含特殊字符，命令行执行失败

**解决方案：**
```bash
# 使用交互式登录
mysql -u root -p
# 在提示符下输入密码

# 或使用配置文件
cat > ~/.my.cnf << EOF
[client]
user=root
password=your_password
EOF

# 然后直接运行
mysql goodservices < db_optimization.sql
```

---

## 应用集成指南

### 后端（Python/FastAPI）

**1. 更新SQLAlchemy模型**

```python
from sqlalchemy import Column, String, Integer, DateTime, Index, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class BUser(Base):
    __tablename__ = "buser_table"

    id = Column(Integer, primary_key=True, index=True)
    uname = Column(String(255), unique=True, nullable=False, index=True)
    ctype = Column(String(255), nullable=False, default="身份证")
    idno = Column(String(255), unique=True, nullable=False)
    bname = Column(String(50), nullable=False)
    bpwd = Column(String(255), nullable=False)  # 已扩大，支持BCrypt
    phoneNo = Column(String(20), unique=True, nullable=False)
    rdate = Column(DateTime, nullable=False)
    udate = Column(DateTime, nullable=True)
    userlvl = Column(String(8), nullable=True)
    desc = Column(String(255), nullable=True)

class Report(Base):
    __tablename__ = "report"

    monthID = Column(String(6), primary_key=True)
    stype_id = Column(Integer, primary_key=True)
    cityID = Column(String(255), primary_key=True)
    ps_num = Column(Integer, nullable=False)
    rs_num = Column(Integer, nullable=False)
```

**2. 更新Pydantic Schema**

```python
from pydantic import BaseModel, Field, field_validator
import re

class UserRegisterRequest(BaseModel):
    uname: str = Field(..., min_length=3, max_length=20)
    idno: str = Field(..., regex=r"^\d{18}$")
    bname: str = Field(..., min_length=2, max_length=20)
    bpwd: str = Field(..., min_length=6, max_length=20)
    phoneNo: str = Field(..., regex=r"^1[3-9]\d{9}$")

    @field_validator("bpwd")
    @classmethod
    def validate_password(cls, v):
        # 密码必须包含大小写字母和数字
        if not re.search(r"[A-Z]", v):
            raise ValueError("密码必须包含大写字母")
        if not re.search(r"[a-z]", v):
            raise ValueError("密码必须包含小写字母")
        if not re.search(r"\d", v):
            raise ValueError("密码必须包含数字")
        return v
```

**3. 处理唯一约束冲突**

```python
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

@router.post("/register")
def register(user: UserRegisterRequest, db: Session = Depends(get_db)):
    try:
        db_user = create_user(db, user)
        return {"code": 200, "message": "注册成功"}
    except IntegrityError as e:
        db.rollback()
        # 判断哪个唯一约束冲突
        if "uk_uname" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        elif "uk_phoneNo" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="手机号已注册"
            )
        elif "uk_idno" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="身份证号已注册"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="数据重复，注册失败"
            )
```

---

## 测试用例

### 登录测试

```bash
# 使用cURL测试登录
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user_zhang",
    "password": "Pass123"
  }'

# 预期返回：
# {
#   "code": 200,
#   "message": "登录成功",
#   "data": {
#     "token": "eyJhbGc...",
#     "user_info": {
#       "id": 1,
#       "uname": "user_zhang",
#       "bname": "张三",
#       "phoneNo": "13801111111",
#       "userlvl": "普通用户"
#     }
#   }
# }
```

### 数据查询测试

```bash
# 查询所有用户
curl http://localhost:8000/api/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN"

# 查询服务需求列表
curl http://localhost:8000/api/v1/service-requests?page=1&size=10 \
  -H "Authorization: Bearer YOUR_TOKEN"

# 查询月度统计
curl "http://localhost:8000/api/v1/stats/monthly?start_month=202506&end_month=202511" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 性能验证

### 查询性能测试

```sql
-- 测试1：查询活跃需求（使用新索引）
EXPLAIN SELECT * FROM sr_info
WHERE ps_state = 0 AND ps_begindate <= NOW()
ORDER BY ps_begindate DESC
LIMIT 20;

-- 预期：Using index range scan（使用idx_sr_state_date）

-- 测试2：统计查询（使用新索引）
EXPLAIN SELECT stype_id, COUNT(*) FROM sr_info
WHERE cityID = 110100 AND ps_state = 0
GROUP BY stype_id;

-- 预期：Using index（使用idx_sr_city_type）

-- 测试3：响应查询（使用新索引）
EXPLAIN SELECT * FROM response_info
WHERE response_state = 0
ORDER BY response_date DESC;

-- 预期：Using index（使用idx_response_state）
```

### 基准测试

```bash
# 使用mysqlslap工具进行压测
mysqlslap \
  --user=root \
  --password \
  --host=localhost \
  --concurrency=10 \
  --iterations=100 \
  --query="SELECT * FROM sr_info WHERE ps_state = 0 LIMIT 10" \
  goodservices

# 记录运行时间，与优化前对比
```

---

## 回滚方案（如需恢复）

### 完全回滚

```bash
# 使用之前的备份恢复
mysql -u root -p goodservices < backup_goodservices_20251118_000000.sql
```

### 部分回滚（不推荐）

```sql
-- 删除新增索引
DROP INDEX idx_sr_state_date ON sr_info;
DROP INDEX idx_sr_city_type ON sr_info;
DROP INDEX idx_response_state ON response_info;
DROP INDEX idx_response_sr ON response_info;
DROP INDEX idx_accept_date ON accept_info;

-- 删除约束
ALTER TABLE buser_table DROP CONSTRAINT uk_uname;
ALTER TABLE buser_table DROP CONSTRAINT uk_phoneNo;
ALTER TABLE buser_table DROP CONSTRAINT uk_idno;
ALTER TABLE sr_info DROP CONSTRAINT chk_sr_state;
ALTER TABLE response_info DROP CONSTRAINT chk_response_state;

-- 恢复字段长度
ALTER TABLE buser_table MODIFY COLUMN bpwd VARCHAR(32);
ALTER TABLE response_info MODIFY COLUMN `desc` TINYINT(0);

-- 恢复主键
ALTER TABLE report DROP PRIMARY KEY;
ALTER TABLE report ADD PRIMARY KEY (monthID);
```

---

## 文件清单

| 文件名 | 大小 | 用途 | 执行顺序 |
|--------|------|------|--------|
| db_optimization.sql | 5.7KB | 数据库优化 | 1 |
| test_data.sql | 16KB | 测试数据导入 | 2 |
| goodservices.sql | 9.1KB | 原始schema | 参考 |
| DATABASE_OPTIMIZATION_SUMMARY.md | 17KB | 详细说明 | 参考 |
| DATABASE_SETUP_GUIDE.md | 本文档 | 快速指南 | 执行指南 |

---

## 获取帮助

### 常用命令

```bash
# 查看数据库字符集
mysql -u root -p -e "SHOW CREATE DATABASE goodservices;"

# 查看表结构
mysql -u root -p -e "DESCRIBE goodservices.buser_table;"

# 查看索引
mysql -u root -p -e "SHOW KEYS FROM goodservices.sr_info;"

# 查看约束
mysql -u root -p -e "SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE TABLE_SCHEMA='goodservices';"

# 导出现有数据
mysqldump -u root -p goodservices > current_state.sql
```

### 联系支持

- 文档：`DATABASE_OPTIMIZATION_SUMMARY.md`
- 技术方案：`technical_solution.md`
- 数据库设计：`goodservices_database_documentation.md`

---

**最后更新：** 2025-11-18
**状态：** 生产就绪 ✓
