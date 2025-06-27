"""
Config表使用示例
这个文件展示了如何使用config表进行各种操作。
"""

from langflow.services.database.models.config.crud import (
    create_config,
    delete_config,
    get_config_by_id,
    get_config_by_key,
    get_config_value,
    get_configs,
    set_config_value,
    update_config,
)
from langflow.services.database.models.config.model import ConfigCreate, ConfigUpdate
from langflow.services.deps import session_scope


async def example_basic_operations():
    """基本的CRUD操作示例"""
    
    async with session_scope() as session:
        # 1. 创建配置项
        config_data = ConfigCreate(key="app_name", value="WorldSeek Flow")
        new_config = await create_config(session, config_data)
        print(f"Created config: {new_config.id} - {new_config.key}: {new_config.value}")
        
        # 2. 通过ID获取配置
        config = await get_config_by_id(session, new_config.id)
        print(f"Get by ID: {config.key}: {config.value}")
        
        # 3. 通过key获取配置
        config = await get_config_by_key(session, "app_name")
        print(f"Get by key: {config.key}: {config.value}")
        
        # 4. 更新配置
        update_data = ConfigUpdate(value="WorldSeek Flow v2.0")
        updated_config = await update_config(session, config, update_data)
        print(f"Updated: {updated_config.key}: {updated_config.value}")
        
        # 5. 获取所有配置（带分页）
        all_configs = await get_configs(session, skip=0, limit=10)
        print(f"Found {len(all_configs)} configs")
        
        # 6. 删除配置
        success = await delete_config(session, new_config.id)
        print(f"Deleted: {success}")


async def example_convenience_methods():
    """便捷方法示例"""
    
    async with session_scope() as session:
        # 1. 设置配置值（如果不存在则创建，存在则更新）
        config = await set_config_value(session, "max_users", "100")
        print(f"Set value: {config.key}: {config.value}")
        
        # 2. 获取配置值（带默认值）
        value = await get_config_value(session, "max_users", "50")
        print(f"Max users: {value}")
        
        # 3. 获取不存在的配置值
        value = await get_config_value(session, "non_existent", "default_value")
        print(f"Non-existent config: {value}")
        
        # 4. 更新配置值
        updated_config = await set_config_value(session, "max_users", "200")
        print(f"Updated value: {updated_config.value}")


async def example_search_and_filter():
    """搜索和过滤示例"""
    
    async with session_scope() as session:
        # 创建一些测试配置
        test_configs = [
            ConfigCreate(key="database_host", value="localhost"),
            ConfigCreate(key="database_port", value="5432"),
            ConfigCreate(key="redis_host", value="localhost"),
            ConfigCreate(key="redis_port", value="6379"),
            ConfigCreate(key="app_debug", value="true"),
        ]
        
        for config_data in test_configs:
            await create_config(session, config_data)
        
        # 搜索包含"database"的配置
        db_configs = await get_configs(session, key_filter="database")
        print(f"Database configs: {[c.key for c in db_configs]}")
        
        # 搜索包含"port"的配置
        port_configs = await get_configs(session, key_filter="port")
        print(f"Port configs: {[c.key for c in port_configs]}")
        
        # 获取前3个配置
        limited_configs = await get_configs(session, limit=3)
        print(f"Limited configs: {[c.key for c in limited_configs]}")


if __name__ == "__main__":
    import asyncio
    
    print("=== 基本操作示例 ===")
    asyncio.run(example_basic_operations())
    
    print("\\n=== 便捷方法示例 ===")
    asyncio.run(example_convenience_methods())
    
    print("\\n=== 搜索过滤示例 ===")
    asyncio.run(example_search_and_filter()) 