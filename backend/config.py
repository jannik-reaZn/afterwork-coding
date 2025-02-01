from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Afterwork Coding"
    cors_origins: list = ["http://127.0.0.1:5173", "http://localhost:5173"]
    verbose_database_logging: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
settingsDep = Annotated[Settings, Depends(get_settings)]
