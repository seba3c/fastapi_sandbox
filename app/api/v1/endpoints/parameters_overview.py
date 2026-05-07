from fastapi import APIRouter


router = APIRouter(tags=["parameters_overview"])


@router.post("")
async def parameters_overview():
    return {}
