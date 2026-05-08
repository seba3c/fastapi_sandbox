from datetime import datetime

from pydantic import Field

from app.schemas.base import BaseModel


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50)


class Category(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50)
    created_at: datetime
    updated_at: datetime
