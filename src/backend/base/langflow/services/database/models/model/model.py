from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class ModelBase(SQLModel):
    name: str = Field(index=True, max_length=255, description="模型显示名称")
    model_id: str = Field(index=True, max_length=255, description="模型实际请求ID")
    api_path: str = Field(max_length=500, description="API路径")
    api_key: str = Field(max_length=500, description="API密钥")


class Model(ModelBase, table=True):  # type: ignore[call-arg]
    __tablename__ = "model"
    
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ModelCreate(ModelBase):
    pass


class ModelRead(ModelBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ModelUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=255, description="模型显示名称")
    model_id: Optional[str] = Field(default=None, max_length=255, description="模型实际请求ID")
    api_path: Optional[str] = Field(default=None, max_length=500, description="API路径")
    api_key: Optional[str] = Field(default=None, max_length=500, description="API密钥") 