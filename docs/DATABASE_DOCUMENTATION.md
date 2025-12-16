# GoodServices 数据库设计说明文档

**数据库名称：** goodservices
**数据库类型：** MySQL 8.0
**创建日期：** 2025-11-06
**用途：** 社区便民服务撮合平台

---

## 一、系统概述

### 1.1 业务描述
GoodServices 是一个 **O2O 社区服务撮合平台**，类似于"邻里互助"或"本地服务平台"。

**核心功能：**
- 用户发布服务需求（如需要管道维修、助老服务等）
- 其他用户浏览并响应服务需求
- 需求发布者选择合适的服务提供者
- 记录服务达成情况
- 按月度、城市、服务类型统计数据

### 1.2 典型业务流程

```
用户A发布需求 → 用户B/C/D响应 → 用户A选择接受用户B → 服务达成 → 月度统计
```

**具体示例：**
1. 张三发布需求："厨房水管漏水，需要维修"
2. 李四响应："我是专业水管工，30分钟内上门"
3. 张三接受李四的响应
4. 服务完成，系统记录此次服务
5. 月底统计：北京市11月管道维修需求+1，成功服务+1

---

## 二、数据库架构

### 2.1 数据表清单

| 表名 | 说明 | 记录数 |
|------|------|--------|
| auser_table | 管理员用户表 | 1条 |
| buser_table | 业务用户表 | 0条（空表） |
| service_type | 服务类型表 | 6条 |
| sr_info | 服务需求发布表 | 0条（空表） |
| response_info | 服务响应表 | 0条（空表） |
| accept_info | 服务达成记录表 | 0条（空表） |
| city_info | 城市信息表 | 0条（空表） |
| report | 月度统计报表 | 0条（空表） |

### 2.2 表关系图

```
┌─────────────────┐
│  auser_table    │  管理员表
│  (管理员登录)    │
└─────────────────┘

┌─────────────────┐
│  buser_table    │  业务用户表（核心）
│  (用户信息)      │
└────────┬────────┘
         │
         ├──────────────────┐
         │                  │
         ↓                  ↓
┌─────────────────┐  ┌──────────────────┐
│   sr_info       │  │  response_info   │  服务响应表
│  (服务需求发布)  │←─│  (响应服务需求)   │
└────────┬────────┘  └─────────┬────────┘
         │                     │
         └──────────┬──────────┘
                    ↓
          ┌──────────────────┐
          │   accept_info    │  服务达成记录表
          │  (服务成功记录)   │
          └──────────────────┘

┌─────────────────┐
│  service_type   │  服务类型表（字典）
│  (6种服务类型)   │
└────────┬────────┘
         │
         └──→ sr_info (外键关联)

┌─────────────────┐
│   city_info     │  城市信息表（字典）
│  (城市数据)      │
└────────┬────────┘
         │
         └──→ sr_info (业务关联)

┌─────────────────┐
│     report      │  月度统计报表
│  (数据分析统计)  │
└─────────────────┘
```

---

## 三、数据表详细设计

### 3.1 用户管理模块

#### auser_table - 管理员用户表

**用途：** 系统管理员登录账号

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|---------|------|------|
| aname | VARCHAR(50) | PRIMARY KEY | 管理员用户名 |
| apwd | VARCHAR(50) | NOT NULL | 管理员密码 |

**初始数据：**
- 用户名：admin
- 密码：admin

---

#### buser_table - 业务用户表 ⭐核心表

**用途：** 平台注册用户信息

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|---------|------|------|
| id | INT | PRIMARY KEY AUTO_INCREMENT | 用户唯一标识 |
| uname | VARCHAR(255) | NOT NULL | 用户注册名称 |
| ctype | VARCHAR(255) | NOT NULL | 证件类型（默认：身份证） |
| idno | VARCHAR(255) | NOT NULL | 证件号码 |
| bname | VARCHAR(50) | NOT NULL | 用户真实姓名 |
| bpwd | VARCHAR(32) | NOT NULL | 登录密码（建议MD5加密） |
| phoneNo | VARCHAR(20) | NOT NULL | 联系电话 |
| rdate | DATETIME | NOT NULL | 注册时间 |
| udate | DATETIME | NULL | 最后修改时间 |
| userlvl | VARCHAR(8) | NULL | 用户级别（可扩展：普通/VIP等） |
| desc | VARCHAR(255) | NULL | 用户简介 |

**业务规则：**
- 用户名、证件号、手机号应唯一
- 密码需加密存储
- 用户级别可用于权限管理或增值服务

---

### 3.2 服务需求模块

#### service_type - 服务类型表（字典表）

**用途：** 定义平台支持的服务类型

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|---------|------|------|
| id | INT | PRIMARY KEY AUTO_INCREMENT | 服务类型标识 |
| typename | VARCHAR(50) | NOT NULL | 服务类型名称 |

**当前服务类型：**
1. 管道维修
2. 助老服务
3. 保洁服务
4. 就诊服务
5. 营养餐服务
6. 定期接送服务

---

#### sr_info - 服务需求发布表 ⭐核心表

**用途：** 用户发布的服务需求信息

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|---------|------|------|
| sr_id | INT | PRIMARY KEY AUTO_INCREMENT | 服务需求唯一标识 |
| sr_title | VARCHAR(80) | NOT NULL | 服务需求标题 |
| stype_id | INT | NOT NULL, FK | 服务类型（外键→service_type.id） |
| psr_userid | INT | NOT NULL, FK | 发布用户（外键→buser_table.id） |
| cityID | INT | NOT NULL | 服务所在城市 |
| desc | VARCHAR(300) | NOT NULL | 服务详细描述 |
| file_list | VARCHAR(300) | NOT NULL | 图片/文件列表（逗号分隔） |
| ps_begindate | DATETIME | NOT NULL | 发布日期（默认当前时间） |
| ps_state | INT | NOT NULL | 状态：0=已发布，-1=已取消 |
| ps_updatedate | DATETIME | NULL | 最后修改时间 |

**外键约束：**
- `psr_userid` → `buser_table.id` (发布者必须是注册用户)
- `stype_id` → `service_type.id` (必须是有效的服务类型)

**索引：**
- INDEX on `psr_userid` (查询某用户发布的所有需求)
- INDEX on `stype_id` (查询某类型的所有需求)

---

### 3.3 服务响应模块

#### response_info - 服务响应表 ⭐核心表

**用途：** 用户对服务需求的响应信息

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|---------|------|------|
| response_id | INT | PRIMARY KEY AUTO_INCREMENT | 响应唯一标识 |
| response_userid | INT | NOT NULL, FK | 响应用户（外键→buser_table.id） |
| sr_id | INT | NOT NULL | 对应的服务需求ID |
| title | VARCHAR(50) | NOT NULL | 响应标题 |
| desc | TINYINT | NOT NULL | 响应描述 |
| response_date | DATETIME | NOT NULL | 响应日期 |
| response_state | INT | NOT NULL | 响应状态（见下方） |
| update_date | DATETIME | NULL | 最后修改时间 |
| file_list | VARCHAR(400) | NOT NULL | 介绍图片等文件列表 |

**响应状态说明：**
- `0` - 待接受（已响应，等待需求发布者确认）
- `1` - 已接受（需求发布者接受此响应）
- `2` - 已拒绝（需求发布者拒绝此响应）
- `3` - 已取消（响应者主动取消）

**外键约束：**
- `response_userid` → `buser_table.id` (响应者必须是注册用户)

**业务规则：**
- 一个服务需求可以有多个响应
- 同一用户可对同一需求响应多次（不推荐）
- 需求发布者不能响应自己的需求（业务层控制）

---

### 3.4 服务达成模块

#### accept_info - 服务达成记录表

**用途：** 记录服务成功达成的信息

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|---------|------|------|
| id | INT | PRIMARY KEY | 记录唯一标识 |
| srid | INT | NOT NULL, FK | 服务需求标识（外键→sr_info.sr_id） |
| psr_userid | INT | NOT NULL | 发布需求用户 |
| response_id | INT | NOT NULL, FK | 服务响应标识（外键→response_info.response_id） |
| response_userid | INT | NOT NULL | 响应用户 |
| createdate | DATETIME | NOT NULL | 服务达成日期 |
| desc | INT | NULL | 备注描述 |

**外键约束：**
- `srid` → `sr_info.sr_id`
- `response_id` → `response_info.response_id`

**索引：**
- INDEX on `srid` (查询某需求的达成记录)
- INDEX on `response_id` (查询某响应是否达成)

**业务规则：**
- 一个服务需求只能有一条达成记录
- 达成后，对应的 response_info.response_state 应为 1（已接受）

---

### 3.5 基础数据模块

#### city_info - 城市信息表

**用途：** 城市和省份基础数据

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|---------|------|------|
| cityID | INT | PRIMARY KEY | 城市编码（国标码） |
| cityName | VARCHAR(255) | NULL | 城市名称 |
| provinceID | INT | NULL | 省份编码 |
| provinceName | VARCHAR(255) | NULL | 省份名称 |

**用途：**
- 服务需求地域定位
- 数据统计分析（按城市统计）
- 可扩展为三级联动（省-市-区）

---

### 3.6 统计分析模块

#### report - 月度统计报表

**用途：** 按月份、服务类型、城市统计服务数据

| 字段名 | 数据类型 | 约束 | 说明 |
|--------|---------|------|------|
| monthID | VARCHAR(6) | PRIMARY KEY | 统计月份（格式：YYYYMM，如：202511） |
| stype_id | INT | NOT NULL | 服务类型标识 |
| cityID | VARCHAR(255) | NOT NULL | 城市编码 |
| ps_num | INT | NOT NULL | 月累计发布服务需求数 |
| rs_num | INT | NOT NULL | 月累计响应成功服务数 |

**统计维度：**
- 时间维度：月份
- 服务维度：服务类型
- 地域维度：城市

**生成方式：**
- 可通过定时任务（Cron Job）每月1号统计上月数据
- 或使用数据库触发器实时累加

---

## 四、业务场景详解

### 4.1 用户注册流程

```sql
-- 1. 用户填写注册信息
INSERT INTO buser_table (uname, ctype, idno, bname, bpwd, phoneNo, rdate, userlvl)
VALUES ('zhangsan', '身份证', '110101199001011234', '张三', MD5('password123'), '13800138000', NOW(), '普通用户');
```

### 4.2 发布服务需求流程

```sql
-- 1. 张三发布管道维修需求
INSERT INTO sr_info (sr_title, stype_id, psr_userid, cityID, `desc`, file_list, ps_begindate, ps_state)
VALUES (
    '厨房水管漏水急需维修',
    1,  -- 管道维修
    1,  -- 张三的用户ID
    110100,  -- 北京市
    '厨房水龙头下方水管破裂，需要专业人员上门维修',
    'leak1.jpg,leak2.jpg',
    NOW(),
    0  -- 已发布
);
```

### 4.3 响应服务需求流程

```sql
-- 1. 李四响应张三的需求
INSERT INTO response_info (response_userid, sr_id, title, `desc`, response_date, response_state, file_list)
VALUES (
    2,  -- 李四的用户ID
    1,  -- 张三发布的需求ID
    '专业水管维修，30分钟上门',
    '从业10年，工具齐全，价格实惠',
    NOW(),
    0,  -- 待接受
    'certificate.jpg,toolbox.jpg'
);
```

### 4.4 接受响应并达成服务

```sql
-- 1. 张三接受李四的响应
UPDATE response_info SET response_state = 1 WHERE response_id = 1;

-- 2. 记录服务达成
INSERT INTO accept_info (id, srid, psr_userid, response_id, response_userid, createdate)
VALUES (1, 1, 1, 1, 2, NOW());

-- 3. 更新服务需求状态为已取消（已达成，不再接受新响应）
UPDATE sr_info SET ps_state = -1 WHERE sr_id = 1;
```

### 4.5 月度数据统计

```sql
-- 统计2025年11月北京市管道维修服务数据
INSERT INTO report (monthID, stype_id, cityID, ps_num, rs_num)
SELECT
    '202511',
    1,  -- 管道维修
    '110100',  -- 北京
    COUNT(DISTINCT sr.sr_id) AS ps_num,  -- 发布需求数
    COUNT(DISTINCT ai.id) AS rs_num      -- 成功服务数
FROM sr_info sr
LEFT JOIN accept_info ai ON sr.sr_id = ai.srid
WHERE sr.stype_id = 1
  AND sr.cityID = 110100
  AND DATE_FORMAT(sr.ps_begindate, '%Y%m') = '202511';
```

---

## 五、数据库优化建议

### 5.1 索引优化

**已有索引：**
- 各表主键索引
- sr_info: `psr_userid`, `stype_id`
- response_info: `response_userid`
- accept_info: `srid`, `response_id`

**建议新增索引：**
```sql
-- 1. 服务需求状态查询优化
CREATE INDEX idx_sr_state ON sr_info(ps_state, ps_begindate);

-- 2. 服务响应状态查询优化
CREATE INDEX idx_response_state ON response_info(response_state, response_date);

-- 3. 城市服务需求查询优化
CREATE INDEX idx_sr_city ON sr_info(cityID, stype_id);

-- 4. 用户登录优化
CREATE UNIQUE INDEX idx_buser_phone ON buser_table(phoneNo);
CREATE UNIQUE INDEX idx_buser_uname ON buser_table(uname);
```

### 5.2 数据完整性

**建议添加约束：**
```sql
-- 1. 用户手机号唯一
ALTER TABLE buser_table ADD UNIQUE(phoneNo);

-- 2. 用户名唯一
ALTER TABLE buser_table ADD UNIQUE(uname);

-- 3. 响应状态检查
ALTER TABLE response_info ADD CHECK (response_state IN (0, 1, 2, 3));

-- 4. 服务需求状态检查
ALTER TABLE sr_info ADD CHECK (ps_state IN (0, -1));
```

### 5.3 性能优化

**分区策略：**
```sql
-- 按月份分区 report 表
ALTER TABLE report PARTITION BY RANGE (monthID) (
    PARTITION p202501 VALUES LESS THAN ('202502'),
    PARTITION p202502 VALUES LESS THAN ('202503'),
    -- ...
);
```

### 5.4 安全性建议

1. **密码加密：** bpwd 字段应存储加密后的密码（MD5/SHA256/bcrypt）
2. **敏感信息：** idno（证件号）应加密存储
3. **SQL注入防护：** 使用参数化查询
4. **权限控制：** 业务用户不应有 DROP/TRUNCATE 权限

---

## 六、扩展功能建议

### 6.1 评价系统
```sql
CREATE TABLE rating_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    accept_id INT NOT NULL,  -- 关联 accept_info
    rater_userid INT NOT NULL,  -- 评价人
    rated_userid INT NOT NULL,  -- 被评价人
    rating TINYINT NOT NULL,  -- 评分（1-5星）
    comment VARCHAR(500),  -- 评价内容
    create_date DATETIME NOT NULL,
    FOREIGN KEY (accept_id) REFERENCES accept_info(id)
);
```

### 6.2 消息通知表
```sql
CREATE TABLE notification (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,  -- 接收通知的用户
    type VARCHAR(20) NOT NULL,  -- 通知类型（新响应/被接受等）
    content VARCHAR(255) NOT NULL,  -- 通知内容
    is_read TINYINT DEFAULT 0,  -- 是否已读
    create_date DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES buser_table(id)
);
```

### 6.3 用户钱包/积分
```sql
CREATE TABLE user_wallet (
    user_id INT PRIMARY KEY,
    balance DECIMAL(10, 2) DEFAULT 0.00,  -- 余额
    points INT DEFAULT 0,  -- 积分
    FOREIGN KEY (user_id) REFERENCES buser_table(id)
);
```

---

## 七、常用查询SQL

### 7.1 查询某用户发布的所有需求
```sql
SELECT sr.*, st.typename, u.bname AS publisher_name
FROM sr_info sr
JOIN service_type st ON sr.stype_id = st.id
JOIN buser_table u ON sr.psr_userid = u.id
WHERE sr.psr_userid = 1  -- 用户ID
ORDER BY sr.ps_begindate DESC;
```

### 7.2 查询某需求的所有响应
```sql
SELECT r.*, u.bname AS responder_name, u.phoneNo
FROM response_info r
JOIN buser_table u ON r.response_userid = u.id
WHERE r.sr_id = 1  -- 需求ID
  AND r.response_state != 3  -- 排除已取消的响应
ORDER BY r.response_date ASC;
```

### 7.3 查询某用户的服务达成记录
```sql
-- 作为服务提供者
SELECT ai.*, sr.sr_title, u.bname AS requester_name
FROM accept_info ai
JOIN sr_info sr ON ai.srid = sr.sr_id
JOIN buser_table u ON ai.psr_userid = u.id
WHERE ai.response_userid = 2  -- 服务提供者ID
ORDER BY ai.createdate DESC;
```

### 7.4 统计各服务类型的需求数量
```sql
SELECT st.typename, COUNT(sr.sr_id) AS request_count
FROM service_type st
LEFT JOIN sr_info sr ON st.id = sr.stype_id
GROUP BY st.id, st.typename
ORDER BY request_count DESC;
```

### 7.5 查询活跃用户排行榜
```sql
-- 发布需求最多的用户
SELECT u.bname, u.phoneNo, COUNT(sr.sr_id) AS request_count
FROM buser_table u
JOIN sr_info sr ON u.id = sr.psr_userid
GROUP BY u.id
ORDER BY request_count DESC
LIMIT 10;

-- 响应服务最多的用户
SELECT u.bname, u.phoneNo, COUNT(r.response_id) AS response_count
FROM buser_table u
JOIN response_info r ON u.id = r.response_userid
GROUP BY u.id
ORDER BY response_count DESC
LIMIT 10;
```

---

## 八、附录

### 8.1 数据字典快速参考

| 表名 | 中文名 | 主键 | 主要外键 |
|------|--------|------|----------|
| auser_table | 管理员表 | aname | - |
| buser_table | 用户表 | id | - |
| service_type | 服务类型 | id | - |
| sr_info | 服务需求 | sr_id | psr_userid→buser, stype_id→service_type |
| response_info | 服务响应 | response_id | response_userid→buser |
| accept_info | 服务达成 | id | srid→sr_info, response_id→response_info |
| city_info | 城市信息 | cityID | - |
| report | 月度报表 | monthID | - |

### 8.2 状态码对照表

**sr_info.ps_state (服务需求状态):**
- `0` - 已发布（活跃状态，可接受响应）
- `-1` - 已取消（不再接受响应）

**response_info.response_state (响应状态):**
- `0` - 待接受（等待需求发布者确认）
- `1` - 已接受（服务达成）
- `2` - 已拒绝（需求发布者拒绝）
- `3` - 已取消（响应者主动取消）

### 8.3 文件存储说明

**file_list 字段格式：**
- 多个文件用逗号分隔：`"file1.jpg,file2.png,file3.pdf"`
- 建议存储相对路径或文件ID
- 实际文件存储在文件服务器或对象存储（OSS）

**建议存储格式：**
```
uploads/sr/{sr_id}/{timestamp}_{filename}
uploads/response/{response_id}/{timestamp}_{filename}
```

---

## 九、总结

### 9.1 优点
- ✅ 表结构清晰，职责明确
- ✅ 外键约束完整，数据一致性好
- ✅ 业务流程完整（发布→响应→达成）
- ✅ 支持数据统计分析

### 9.2 待完善
- ⚠️ 缺少评价系统
- ⚠️ 缺少消息通知机制
- ⚠️ 缺少支付/钱包功能
- ⚠️ 敏感信息未加密
- ⚠️ 缺少用户唯一性约束（手机号、用户名）
- ⚠️ report 表主键设计不合理（应为复合主键）

### 9.3 推荐改进
```sql
-- 修改 report 表主键
ALTER TABLE report DROP PRIMARY KEY;
ALTER TABLE report ADD PRIMARY KEY (monthID, stype_id, cityID);
```

---

**文档版本：** v1.0
**最后更新：** 2025-11-17
**维护者：** Claude Code
