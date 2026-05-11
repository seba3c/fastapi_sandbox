class EntityDuplicatedError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class CategoryDuplicatedError(EntityDuplicatedError):
    def __init__(self):
        super().__init__("Category with this name already exists.")
