from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger
from sqlalchemy.exc import IntegrityError

from langflow.api.utils import DbSession
from langflow.services.auth.utils import get_current_active_user
from langflow.services.database.models.model.crud import (
    create_model,
    delete_model,
    get_model_by_id,
    get_model_by_name,
    get_models,
    update_model,
)
from langflow.services.database.models.model.model import Model, ModelCreate, ModelRead, ModelUpdate

router = APIRouter(tags=["Models"], prefix="/models")


@router.post("/", response_model=ModelRead, status_code=201)
async def create_model_endpoint(
    model: ModelCreate,
    session: DbSession,
    current_user=Depends(get_current_active_user),
) -> Model:
    """创建新的模型配置"""
    try:
        logger.info(f"User {current_user.username if current_user else 'Unknown'} creating model: {model.name}")
        return await create_model(session, model)
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f"创建模型配置失败")
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        raise HTTPException(status_code=500, detail="创建模型配置失败")


@router.get("/", response_model=list[ModelRead])
async def get_models_endpoint(
    session: DbSession,
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的最大记录数"),
    name_filter: Optional[str] = Query(None, description="按模型名称过滤（支持模糊匹配）"),
    current_user=Depends(get_current_active_user),
) -> list[Model]:
    """获取模型配置列表，支持分页和过滤"""
    try:
        logger.debug(f"User {current_user.username if current_user else 'Unknown'} fetching models")
        return await get_models(session, skip=skip, limit=limit, name_filter=name_filter)
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        raise HTTPException(status_code=500, detail="获取模型配置列表失败")


@router.get("/{model_id}", response_model=ModelRead)
async def get_model_endpoint(
    model_id: int,
    session: DbSession,
    current_user=Depends(get_current_active_user),
) -> Model:
    """根据ID获取模型配置"""
    try:
        model = await get_model_by_id(session, model_id)
        if not model:
            raise HTTPException(status_code=404, detail="模型配置未找到")
        logger.debug(f"User {current_user.username if current_user else 'Unknown'} fetched model: {model_id}")
        return model
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching model {model_id}: {e}")
        raise HTTPException(status_code=500, detail="获取模型配置失败")


@router.get("/name/{name}", response_model=ModelRead)
async def get_model_by_name_endpoint(
    name: str,
    session: DbSession,
    current_user=Depends(get_current_active_user),
) -> Model:
    """根据名称获取模型配置"""
    try:
        model = await get_model_by_name(session, name)
        if not model:
            raise HTTPException(status_code=404, detail=f"模型配置 '{name}' 未找到")
        logger.debug(f"User {current_user.username if current_user else 'Unknown'} fetched model by name: {name}")
        return model
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching model by name {name}: {e}")
        raise HTTPException(status_code=500, detail="获取模型配置失败")


@router.put("/{model_id}", response_model=ModelRead)
async def update_model_endpoint(
    model_id: int,
    model_update: ModelUpdate,
    session: DbSession,
    current_user=Depends(get_current_active_user),
) -> Model:
    """更新模型配置"""
    try:
        # 检查模型配置是否存在
        existing_model = await get_model_by_id(session, model_id)
        if not existing_model:
            raise HTTPException(status_code=404, detail="模型配置未找到")
        
        logger.info(f"User {current_user.username if current_user else 'Unknown'} updating model: {model_id}")
        return await update_model(session, existing_model, model_update)
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=400, detail="更新模型配置失败")
    except Exception as e:
        logger.error(f"Error updating model {model_id}: {e}")
        raise HTTPException(status_code=500, detail="更新模型配置失败")


@router.delete("/{model_id}", status_code=204)
async def delete_model_endpoint(
    model_id: int,
    session: DbSession,
    current_user=Depends(get_current_active_user),
) -> None:
    """删除模型配置"""
    try:
        success = await delete_model(session, model_id)
        if not success:
            raise HTTPException(status_code=404, detail="模型配置未找到")
        logger.info(f"User {current_user.username if current_user else 'Unknown'} deleted model: {model_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting model {model_id}: {e}")
        raise HTTPException(status_code=500, detail="删除模型配置失败") 