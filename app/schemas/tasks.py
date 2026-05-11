from app.schemas.base import BaseModel


class CategoryCreatedPayload(BaseModel):
    id: int
    name: str
