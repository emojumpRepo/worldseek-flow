# PostgreSQL 设置指南

## 1. 安装 PostgreSQL
```bash
# Windows (使用 Chocolatey)
choco install postgresql

# 或者下载安装包
# https://www.postgresql.org/download/windows/
```

## 2. 创建数据库
```sql
-- 连接到 PostgreSQL
psql -U postgres

-- 创建数据库和用户
CREATE DATABASE langflow_db;
CREATE USER langflow_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE langflow_db TO langflow_user;
```

## 3. 更新配置
修改 `langflow_db_config.env` 文件：

```env
# PostgreSQL 配置
LANGFLOW_DATABASE_URL=postgresql://langflow_user:your_password@localhost:5432/langflow_db

# 优化的连接池配置
LANGFLOW_DB_CONNECTION_SETTINGS={"pool_size": 20, "max_overflow": 50, "pool_timeout": 30, "pool_pre_ping": true, "pool_recycle": 3600, "echo": false}
```

## 4. 启动 Langflow
```bash
uv run langflow run --env-file langflow_db_config.env
```

## PostgreSQL 优势
- 支持更高并发
- 更好的连接池管理
- 更稳定的性能
- 支持复杂查询 