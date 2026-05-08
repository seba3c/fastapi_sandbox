import random

from pydantic import Field

from app.schemas.base import BaseModel


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class CategoryUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=50)


class Category(BaseModel):
    id: int = Field(default_factory=lambda: random.randint(1, 9999))
    name: str = Field(..., min_length=1, max_length=50)
