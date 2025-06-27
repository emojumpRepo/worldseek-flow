from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class ConfigBase(SQLModel):
    key: str = Field(index=True, unique=True, max_length=255)
    value: str = Field(max_length=1000)


class Config(ConfigBase, table=True):  # type: ignore[call-arg]
    __tablename__ = "config"
    
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConfigCreate(ConfigBase):
    pass


class ConfigRead(ConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ConfigUpdate(SQLModel):
    key: Optional[str] = Field(default=None, max_length=255)
    value: Optional[str] = Field(default=None, max_length=1000) 