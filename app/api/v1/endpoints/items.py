from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_item_repository
from app.repositories.items import InMemoryItemRepository
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter(tags=["items"])


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_create: ItemCreate,
    repository: InMemoryItemRepository = Depends(get_item_repository),
):
    service = ItemService(repository)
    return await service.create_item(item_create)


@router.get("", response_model=list[Item])
async def list_items(
    repository: InMemoryItemRepository = Depends(get_item_repository),
):
    service = ItemService(repository)
    return await service.list_items()


@router.get("/{item_id}", response_model=Item)
async def get_item(
    item_id: UUID,
    repository: InMemoryItemRepository = Depends(get_item_repository),
):
    service = ItemService(repository)
    item = await service.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: UUID,
    item_update: ItemUpdate,
    repository: InMemoryItemRepository = Depends(get_item_repository),
):
    service = ItemService(repository)
    item = await service.update_item(item_id, item_update)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: UUID,
    repository: InMemoryItemRepository = Depends(get_item_repository),
):
    service = ItemService(repository)
    deleted = await service.delete_item(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return None
