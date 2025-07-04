#!/bin/bash
set -e

# 检查可用内存
AVAILABLE_MEMORY=$(free -m | awk 'NR==2{printf "%.0f", $7}')
echo "Available memory: ${AVAILABLE_MEMORY}MB"

# 根据可用内存调整配置
if [ "$AVAILABLE_MEMORY" -lt 1024 ]; then
    echo "Warning: Low memory detected. Adjusting configuration..."
    export LANGFLOW_WORKERS=1
    export LANGFLOW_WORKER_TIMEOUT=300
    export LANGFLOW_DB_CONNECTION_SETTINGS='{"pool_size": 10, "max_overflow": 20, "pool_timeout": 30, "pool_pre_ping": true, "pool_recycle": 1800, "echo": false}'
elif [ "$AVAILABLE_MEMORY" -lt 2048 ]; then
    echo "Medium memory detected. Using standard configuration..."
    export LANGFLOW_WORKERS=1
    export LANGFLOW_WORKER_TIMEOUT=600
else
    echo "Sufficient memory detected. Using optimal configuration..."
    export LANGFLOW_WORKERS=2
    export LANGFLOW_WORKER_TIMEOUT=600
fi

# 设置ulimit防止内存问题
ulimit -v 2097152  # 2GB虚拟内存限制

# 等待数据库连接
if [[ "$LANGFLOW_DATABASE_URL" == postgresql* ]]; then
    echo "Waiting for PostgreSQL to be ready..."
    # 提取数据库连接信息
    DB_HOST=$(echo $LANGFLOW_DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    DB_PORT=$(echo $LANGFLOW_DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    # 等待数据库启动
    timeout=60
    while ! nc -z "$DB_HOST" "$DB_PORT" 2>/dev/null; do
        echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
        sleep 2
        timeout=$((timeout - 2))
        if [ $timeout -le 0 ]; then
            echo "Timeout waiting for PostgreSQL"
            exit 1
        fi
    done
    echo "PostgreSQL is ready!"
fi

# 启动langflow
echo "Starting Langflow with workers: $LANGFLOW_WORKERS, timeout: $LANGFLOW_WORKER_TIMEOUT"
exec langflow run --workers "$LANGFLOW_WORKERS" --worker-timeout "$LANGFLOW_WORKER_TIMEOUT" 