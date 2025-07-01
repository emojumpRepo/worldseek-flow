from datetime import datetime, timezone
from typing import Optional

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.attributes import flag_modified
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from langflow.services.database.models.config.model import Config, ConfigCreate, ConfigUpdate


async def create_config(db: AsyncSession, config: ConfigCreate) -> Config:
    """Create a new config entry."""
    logger.debug(f"Creating config with key: {config.key}")
    
    db_config = Config.model_validate(config, from_attributes=True)
    db.add(db_config)
    
    try:
        await db.commit()
        await db.refresh(db_config)
        logger.debug(f"Successfully created config with id: {db_config.id}")
        return db_config
    except IntegrityError:
        await db.rollback()
        logger.error(f"Config with key '{config.key}' already exists")
        raise


async def get_config_by_id(db: AsyncSession, config_id: int) -> Optional[Config]:
    """Get config by ID."""
    stmt = select(Config).where(Config.id == config_id)
    result = await db.exec(stmt)
    return result.first()


async def get_config_by_key(db: AsyncSession, key: str) -> Optional[Config]:
    """Get config by key."""
    stmt = select(Config).where(Config.key == key)
    result = await db.exec(stmt)
    return result.first()


async def get_configs(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100,
    key_filter: Optional[str] = None
) -> list[Config]:
    """Get list of configs with optional filtering and pagination."""
    stmt = select(Config)
    
    if key_filter:
        stmt = stmt.where(Config.key.contains(key_filter))
    
    stmt = stmt.offset(skip).limit(limit).order_by(Config.created_at.desc())
    result = await db.exec(stmt)
    return list(result)


async def update_config(db: AsyncSession, db_config: Config, config_update: ConfigUpdate) -> Config:
    """Update an existing config entry."""
    logger.debug(f"Updating config with id: {db_config.id}")
    
    update_data = config_update.model_dump(exclude_unset=True)
    
    if not update_data:
        logger.debug("No data to update")
        return db_config
    
    for field, value in update_data.items():
        if hasattr(db_config, field) and value is not None:
            setattr(db_config, field, value)
    
    # Update the updated_at timestamp
    db_config.updated_at = datetime.now(timezone.utc)
    flag_modified(db_config, "updated_at")
    
    try:
        await db.commit()
        await db.refresh(db_config)
        logger.debug(f"Successfully updated config with id: {db_config.id}")
        return db_config
    except IntegrityError:
        await db.rollback()
        logger.error(f"Key conflict when updating config with id: {db_config.id}")
        raise


async def delete_config(db: AsyncSession, config_id: int) -> bool:
    """Delete a config entry."""
    logger.debug(f"Deleting config with id: {config_id}")
    
    stmt = select(Config).where(Config.id == config_id)
    result = await db.exec(stmt)
    db_config = result.first()
    
    if not db_config:
        logger.warning(f"Config with id {config_id} not found")
        return False
    
    await db.delete(db_config)
    await db.commit()
    logger.debug(f"Successfully deleted config with id: {config_id}")
    return True


async def get_config_value(db: AsyncSession, key: str, default: Optional[str] = None) -> Optional[str]:
    """Get config value by key."""
    config = await get_config_by_key(db, key)
    return config.value if config else default


async def set_config_value(db: AsyncSession, key: str, value: str) -> Config:
    """Set config value by key. Creates new entry if key doesn't exist, updates if it does."""
    logger.debug(f"Setting config value for key: {key}")
    
    existing_config = await get_config_by_key(db, key)
    
    if existing_config:
        # Update existing config
        config_update = ConfigUpdate(value=value)
        return await update_config(db, existing_config, config_update)
    else:
        # Create new config
        config_create = ConfigCreate(key=key, value=value)
        return await create_config(db, config_create) 