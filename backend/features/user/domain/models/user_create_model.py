from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    id: Optional[int]
    username: str = Field(min_length=1, example="John Doe")
    full_name: str | None = Field(default=None, example="John Doe")
    email: str = Field(min_length=1, example="john.doe@example.com")
    hashed_password: str = Field(min_length=1, example="my_secure_password")
