import logging

from fastapi import APIRouter, BackgroundTasks, Depends, status

from app.api.dependencies import get_category_repository
from app.repositories.categories import CategoryRepository
from app.schemas.category import (
    Category,
    CategoryCreate,
    CategoryList,
    CategoryUpdate,
    CategoryStream,
)
from app.schemas.common import PaginationParams
from app.schemas.tasks import CategoryCreatedPayload
from app.services.category_service import CategoryService
from app.tasks.category_tasks import notify_category_created

router = APIRouter(tags=["categories"])


logger = logging.getLogger(__name__)


@router.post(
    "/admin/categories", response_model=Category, status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_create: CategoryCreate,
    background_tasks: BackgroundTasks,
    repository: CategoryRepository = Depends(get_category_repository),
):
    service = CategoryService(repository)
    category = await service.create_category(category_create)
    background_tasks.add_task(
        notify_category_created,
        CategoryCreatedPayload(id=category.id, name=category.name),
    )
    return category


@router.get("/public/categories", response_model=CategoryList)
async def list_categories(
    params: PaginationParams = Depends(),
    repository: CategoryRepository = Depends(get_category_repository),
):
    service = CategoryService(repository)
    return await service.list_categories(params)


@router.get("/public/categories/stream")
async def stream_categories(
    repository: CategoryRepository = Depends(get_category_repository),
) -> CategoryStream:
    service = CategoryService(repository)
    params = PaginationParams()
    while True:
        results = await service.list_categories(params)
        if not results.items:
            break
        for item in results.items:
            yield Category.model_validate(item)
        params = PaginationParams(
            limit=params.limit, offset=params.offset + params.limit
        )


@router.get("/admin/categories/{category_id}", response_model=Category)
async def get_category(
    category_id: int,
    repository: CategoryRepository = Depends(get_category_repository),
):
    service = CategoryService(repository)
    return await service.get_category(category_id)


@router.put("/admin/categories/{category_id}", response_model=Category)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    repository: CategoryRepository = Depends(get_category_repository),
):
    service = CategoryService(repository)
    return await service.update_category(category_id, category_update)


@router.delete(
    "/admin/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(
    category_id: int,
    repository: CategoryRepository = Depends(get_category_repository),
):
    service = CategoryService(repository)
    await service.delete_category(category_id)
