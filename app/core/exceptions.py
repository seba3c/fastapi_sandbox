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
