from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    status_code: int = 500

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class EntityNotFoundError(AppException):
    status_code = 404


class CategoryNotFoundError(EntityNotFoundError):
    def __init__(self):
        super().__init__("Category not found")


class EntityDuplicatedError(AppException):
    status_code = 409


class CategoryDuplicatedError(EntityDuplicatedError):
    def __init__(self):
        super().__init__("Category with this name already exists.")


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
