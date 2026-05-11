from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_category_repository
from app.repositories.categories import CategoryRepository
from app.schemas.category import Category, CategoryCreate, CategoryList, CategoryUpdate
from app.schemas.common import PaginationParams
from app.services.category_service import CategoryService

router = APIRouter(tags=["categories"])


@router.post(
    "/admin/categories", response_model=Category, status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_create: CategoryCreate,
    repository: CategoryRepository = Depends(get_category_repository),
):
    service = CategoryService(repository)
    return await service.create_category(category_create)


@router.get("/public/categories", response_model=CategoryList)
async def list_categories(
    params: PaginationParams = Depends(),
    repository: CategoryRepository = Depends(get_category_repository),
):
    service = CategoryService(repository)
    return await service.list_categories(params)


@router.get("/admin/categories/{category_id}", response_model=Category)
async def get_category(
    category_id: int,
    repository: CategoryRepository = Depends(get_category_repository),
):
    service = CategoryService(repository)
    category = await service.get_category(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


@router.put("/admin/categories/{category_id}", response_model=Category)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    repository: CategoryRepository = Depends(get_category_repository),
):
    service = CategoryService(repository)
    category = await service.update_category(category_id, category_update)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


@router.delete(
    "/admin/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(
    category_id: int,
    repository: CategoryRepository = Depends(get_category_repository),
):
    service = CategoryService(repository)
    deleted = await service.delete_category(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return None
