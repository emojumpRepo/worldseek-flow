from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from loguru import logger
from sqlalchemy.exc import IntegrityError

from langflow.api.utils import DbSession
from langflow.services.auth.utils import get_current_active_user
from langflow.services.database.models.config.crud import (
    create_config,
    delete_config,
    get_config_by_id,
    get_config_by_key,
    get_configs,
    get_config_value,
    set_config_value,
    update_config,
)
from langflow.services.database.models.config.model import Config, ConfigCreate, ConfigRead, ConfigUpdate

router = APIRouter(tags=["Config"], prefix="/config")


@router.post("/", response_model=ConfigRead, status_code=201)
async def create_config_endpoint(
    config: ConfigCreate,
    session: DbSession,
    current_user=Depends(get_current_active_user),
) -> Config:
    """创建新的配置项"""
    try:
        logger.info(f"User {current_user.username if current_user else 'Unknown'} creating config with key: {config.key}")
        return await create_config(session, config)
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f"配置键 '{config.key}' 已存在")
    except Exception as e:
        logger.error(f"Error creating config: {e}")
        raise HTTPException(status_code=500, detail="创建配置失败")


@router.get("/", response_model=list[ConfigRead])
async def get_configs_endpoint(
    session: DbSession,
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的最大记录数"),
    key_filter: Optional[str] = Query(None, description="按键名过滤（支持模糊匹配）"),
    current_user=Depends(get_current_active_user),
) -> list[Config]:
    """获取配置列表，支持分页和过滤"""
    try:
        logger.debug(f"User {current_user.username if current_user else 'Unknown'} fetching configs")
        return await get_configs(session, skip=skip, limit=limit, key_filter=key_filter)
    except Exception as e:
        logger.error(f"Error fetching configs: {e}")
        raise HTTPException(status_code=500, detail="获取配置列表失败")


@router.get("/{config_id}", response_model=ConfigRead)
async def get_config_endpoint(
    config_id: int,
    session: DbSession,
    current_user=Depends(get_current_active_user),
) -> Config:
    """根据ID获取配置项"""
    try:
        config = await get_config_by_id(session, config_id)
        if not config:
            raise HTTPException(status_code=404, detail="配置项未找到")
        logger.debug(f"User {current_user.username if current_user else 'Unknown'} fetched config: {config_id}")
        return config
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching config {config_id}: {e}")
        raise HTTPException(status_code=500, detail="获取配置失败")


@router.get("/key/{key}", response_model=ConfigRead)
async def get_config_by_key_endpoint(
    key: str,
    session: DbSession,
    current_user=Depends(get_current_active_user),
) -> Config:
    """根据键名获取配置项"""
    try:
        config = await get_config_by_key(session, key)
        if not config:
            raise HTTPException(status_code=404, detail=f"配置键 '{key}' 未找到")
        logger.debug(f"User {current_user.username if current_user else 'Unknown'} fetched config by key: {key}")
        return config
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching config by key {key}: {e}")
        raise HTTPException(status_code=500, detail="获取配置失败")


@router.put("/{config_id}", response_model=ConfigRead)
async def update_config_endpoint(
    config_id: int,
    config_update: ConfigUpdate,
    session: DbSession,
    current_user=Depends(get_current_active_user),
) -> Config:
    """更新配置项"""
    try:
        # 检查配置是否存在
        existing_config = await get_config_by_id(session, config_id)
        if not existing_config:
            raise HTTPException(status_code=404, detail="配置项未找到")
        
        logger.info(f"User {current_user.username if current_user else 'Unknown'} updating config: {config_id}")
        return await update_config(session, existing_config, config_update)
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=400, detail="键名冲突，该键名已存在")
    except Exception as e:
        logger.error(f"Error updating config {config_id}: {e}")
        raise HTTPException(status_code=500, detail="更新配置失败")


@router.delete("/{config_id}", status_code=204)
async def delete_config_endpoint(
    config_id: int,
    session: DbSession,
    current_user=Depends(get_current_active_user),
) -> None:
    """删除配置项"""
    try:
        success = await delete_config(session, config_id)
        if not success:
            raise HTTPException(status_code=404, detail="配置项未找到")
        logger.info(f"User {current_user.username if current_user else 'Unknown'} deleted config: {config_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting config {config_id}: {e}")
        raise HTTPException(status_code=500, detail="删除配置失败")


@router.get("/value/{key}")
async def get_config_value_endpoint(
    key: str,
    session: DbSession,
    default: Optional[str] = Query(None, description="默认值"),
    current_user=Depends(get_current_active_user),
) -> dict[str, Optional[str]]:
    """根据键名获取配置值"""
    try:
        value = await get_config_value(session, key, default)
        logger.debug(f"User {current_user.username if current_user else 'Unknown'} fetched config value for key: {key}")
        return {"key": key, "value": value}
    except Exception as e:
        logger.error(f"Error fetching config value for key {key}: {e}")
        raise HTTPException(status_code=500, detail="获取配置值失败")


@router.post("/value/{key}", response_model=ConfigRead)
async def set_config_value_endpoint(
    key: str,
    session: DbSession,
    value: str = Body(..., embed=True),
    current_user=Depends(get_current_active_user),
) -> Config:
    """设置配置值（如果不存在则创建，存在则更新）"""
    try:
        logger.info(f"User {current_user.username if current_user else 'Unknown'} setting config value for key: {key}")
        return await set_config_value(session, key, value)
    except Exception as e:
        logger.error(f"Error setting config value for key {key}: {e}")
        raise HTTPException(status_code=500, detail="设置配置值失败") 