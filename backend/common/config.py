from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic import Field
from pydantic_settings import BaseSettings  # , SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Afterwork Coding")
    cors_origins: list[str] = ["http://127.0.0.1:5173", "http://localhost:5173"]

    # Read from environment variables
    secret_key_jwt: str = Field(default="test_secret")
    algorithm_jwt: str = Field(default="HS256")
    verbose_database_logging: bool = Field(default=False)

    # model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
SettingsDependency = Annotated[Settings, Depends(get_settings)]
