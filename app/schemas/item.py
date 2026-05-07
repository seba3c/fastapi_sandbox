from uuid import UUID, uuid4

from pydantic import Field

from app.schemas.base import BaseModel


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str = ""


class ItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50)
    description: str | None = None


class Item(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=1, max_length=50)
    description: str = ""
