from asgi_correlation_id import correlation_id
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
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
        headers={"X-Request-ID": correlation_id.get() or ""},
    )


def register_exception_handlers(app: FastAPI) -> None:
    # Registering custom exception handlers from most specific to least specific
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
