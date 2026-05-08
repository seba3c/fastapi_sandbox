from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    """Custom base model for all Pydantic schemas in the app.

    Add global customizations here (e.g., extra='forbid', strict mode,
    custom JSON encoders, or shared validators).
    """

    model_config = {"populate_by_name": True, "from_attributes": True}
