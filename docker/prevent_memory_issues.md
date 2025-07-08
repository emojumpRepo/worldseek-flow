# 防止内存溢出导致SIGKILL错误的配置指南

## 问题描述

当选择无法连接的语言模型时，可能出现以下错误：
```
Worker (pid:XX) was sent SIGKILL! Perhaps out of memory?
```

这个错误通常由以下原因引起：
1. 模型连接失败导致的资源泄漏
2. 重试机制消耗过多内存
3. 超时设置不当

## 解决方案

### 1. 环境变量配置

在您的 `.env` 文件或 Docker 环境中添加以下配置：

```bash
# Worker 配置
LANGFLOW_WORKERS=1
LANGFLOW_WORKER_TIMEOUT=300
LANGFLOW_WORKER_MAX_REQUESTS=100
LANGFLOW_WORKER_MAX_REQUESTS_JITTER=10

# 内存管理
LANGFLOW_MAX_MEMORY_MB=2048
LANGFLOW_CACHE_TYPE=simple
LANGFLOW_LANGCHAIN_CACHE=SimpleCache

# 数据库连接池优化
LANGFLOW_DB_CONNECTION_SETTINGS='{"pool_size": 5, "max_overflow": 10, "pool_timeout": 30, "pool_pre_ping": true, "pool_recycle": 1800, "echo": false}'

# API 超时设置
LANGFLOW_API_TIMEOUT=30
LANGFLOW_MODEL_TIMEOUT=30
```

### 2. Docker 配置

#### docker-compose.yml 示例：

```yaml
version: '3.8'
services:
  langflow:
    image: your-langflow-image
    environment:
      - LANGFLOW_WORKERS=1
      - LANGFLOW_WORKER_TIMEOUT=300
      - LANGFLOW_MAX_MEMORY_MB=2048
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
    ulimits:
      memlock: 2147483648  # 2GB
      nofile: 65536
```

#### 直接 Docker 运行：

```bash
docker run -d \
  --name langflow \
  --memory=2g \
  --memory-swap=2g \
  --cpus=1.0 \
  --ulimit memlock=2147483648:2147483648 \
  -e LANGFLOW_WORKERS=1 \
  -e LANGFLOW_WORKER_TIMEOUT=300 \
  -e LANGFLOW_MAX_MEMORY_MB=2048 \
  your-langflow-image
```

### 3. 系统级别配置

#### 在 Linux 系统上设置内存限制：

```bash
# 编辑 /etc/security/limits.conf
echo "langflow soft memlock 2097152" >> /etc/security/limits.conf
echo "langflow hard memlock 2097152" >> /etc/security/limits.conf

# 设置 systemd 服务限制（如果使用 systemd）
mkdir -p /etc/systemd/system/langflow.service.d/
cat > /etc/systemd/system/langflow.service.d/memory.conf << EOF
[Service]
MemoryMax=2G
MemoryHigh=1.8G
MemorySwapMax=0
TasksMax=100
EOF
```

### 4. 应用程序配置

#### 在代码中添加内存监控：

```python
import psutil
import gc
import os

def check_memory_usage():
    """检查内存使用情况"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_mb = memory_info.rss / 1024 / 1024
    
    if memory_mb > 1500:  # 超过1.5GB时警告
        print(f"警告: 内存使用量过高: {memory_mb:.2f}MB")
        gc.collect()  # 强制垃圾回收
        
    return memory_mb

def safe_model_creation(provider, model_name, **kwargs):
    """安全创建模型，包含内存检查"""
    try:
        check_memory_usage()
        # 创建模型的代码
        return create_model(provider, model_name, **kwargs)
    except Exception as e:
        gc.collect()  # 异常时清理内存
        raise e
```

### 5. 监控和预防

#### 设置内存监控脚本：

```bash
#!/bin/bash
# memory_monitor.sh
while true; do
    memory_usage=$(free | awk '/^Mem:/{printf("%.2f"), $3/$2*100}')
    if (( $(echo "$memory_usage > 85" | bc -l) )); then
        echo "$(date): 内存使用率过高: ${memory_usage}%"
        # 可以在这里添加重启服务的逻辑
        # systemctl restart langflow
    fi
    sleep 30
done
```

### 6. 故障排除

#### 如果仍然遇到SIGKILL错误：

1. **检查系统内存**：
   ```bash
   free -h
   cat /proc/meminfo
   ```

2. **查看进程内存使用**：
   ```bash
   ps aux --sort=-%mem | head -10
   ```

3. **检查 OOM Killer 日志**：
   ```bash
   dmesg | grep -i "killed process"
   journalctl -u langflow | grep -i "memory"
   ```

4. **分析内存泄漏**：
   ```bash
   # 使用 valgrind 或 heaptrack 分析内存使用
   valgrind --tool=massif python -m langflow run
   ```

### 7. 最佳实践

1. **模型选择前验证连接**：在使用模型前先测试API连接
2. **设置合理的超时时间**：避免长时间等待导致资源占用
3. **限制重试次数**：防止无限重试导致内存堆积
4. **定期清理资源**：使用垃圾回收和连接池管理
5. **监控内存使用**：设置阈值警告和自动重启机制

### 8. 紧急恢复

如果系统已经出现SIGKILL错误：

```bash
# 1. 重启服务
systemctl restart langflow
# 或
docker restart langflow

# 2. 清理缓存
rm -rf /tmp/langflow_*
rm -rf ~/.cache/langflow/*

# 3. 重置配置
export LANGFLOW_WORKERS=1
export LANGFLOW_WORKER_TIMEOUT=300

# 4. 重新启动（使用更保守的配置）
langflow run --workers 1 --worker-timeout 300
```

## 结论

通过以上配置和预防措施，可以有效避免因模型连接失败导致的内存溢出问题。关键是限制资源使用、设置合理超时、及时清理资源，并建立有效的监控机制。 