from datetime import datetime, timezone
from typing import Optional

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.attributes import flag_modified
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from langflow.services.database.models.model.model import Model, ModelCreate, ModelUpdate


async def create_model(db: AsyncSession, model: ModelCreate) -> Model:
    """Create a new model entry."""
    logger.debug(f"Creating model with name: {model.name}")
    
    db_model = Model.model_validate(model, from_attributes=True)
    db.add(db_model)
    
    try:
        await db.commit()
        await db.refresh(db_model)
        logger.debug(f"Successfully created model with id: {db_model.id}")
        return db_model
    except IntegrityError:
        await db.rollback()
        logger.error(f"Error creating model with name '{model.name}'")
        raise


async def get_model_by_id(db: AsyncSession, model_id: int) -> Optional[Model]:
    """Get model by ID."""
    stmt = select(Model).where(Model.id == model_id)
    result = await db.exec(stmt)
    return result.first()


async def get_model_by_name(db: AsyncSession, name: str) -> Optional[Model]:
    """Get model by name."""
    stmt = select(Model).where(Model.name == name)
    result = await db.exec(stmt)
    return result.first()


async def get_models(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    name_filter: Optional[str] = None
) -> list[Model]:
    """Get list of models with optional filtering and pagination."""
    stmt = select(Model)
    
    if name_filter:
        stmt = stmt.where(Model.name.contains(name_filter))
    
    stmt = stmt.offset(skip).limit(limit).order_by(Model.created_at.desc())
    result = await db.exec(stmt)
    return list(result)


async def update_model(db: AsyncSession, db_model: Model, model_update: ModelUpdate) -> Model:
    """Update an existing model entry."""
    logger.debug(f"Updating model with id: {db_model.id}")
    
    update_data = model_update.model_dump(exclude_unset=True)
    
    if not update_data:
        logger.debug("No data to update")
        return db_model
    
    for field, value in update_data.items():
        if hasattr(db_model, field) and value is not None:
            setattr(db_model, field, value)
    
    # Update the updated_at timestamp
    db_model.updated_at = datetime.now(timezone.utc)
    flag_modified(db_model, "updated_at")
    
    try:
        await db.commit()
        await db.refresh(db_model)
        logger.debug(f"Successfully updated model with id: {db_model.id}")
        return db_model
    except IntegrityError:
        await db.rollback()
        logger.error(f"Error updating model with id: {db_model.id}")
        raise


async def delete_model(db: AsyncSession, model_id: int) -> bool:
    """Delete a model entry."""
    logger.debug(f"Deleting model with id: {model_id}")
    
    stmt = select(Model).where(Model.id == model_id)
    result = await db.exec(stmt)
    db_model = result.first()
    
    if not db_model:
        logger.warning(f"Model with id {model_id} not found")
        return False
    
    await db.delete(db_model)
    await db.commit()
    logger.debug(f"Successfully deleted model with id: {model_id}")
    return True 