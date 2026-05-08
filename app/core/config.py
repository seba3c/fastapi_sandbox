from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI Sandbox"
    debug: bool = False
    version: str = "0.1"
    environment: Literal["development", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    database_url: str = (
        "mysql+aiomysql://fa_ecom_user:fa_ecom_pass@localhost:3306/fa_ecom"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
