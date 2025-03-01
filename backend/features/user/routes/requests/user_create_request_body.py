from typing import Optional

from pydantic import Field

from backend.common.route.requests import RequestModel
from backend.features.user.domain.models import UserCreate


class UserCreateRequestBody(RequestModel):
    id: Optional[int]
    username: str = Field(title="The username of the user")
    full_name: str | None = Field(title="The full name of the user", default=None, alias="fullName")
    email: str = Field(title="The email address of the user")
    hashed_password: str = Field(title="The encrypted password of the user")

    def to_create_model(self) -> UserCreate:
        return UserCreate(
            id=self.id,
            username=self.username,
            full_name=self.full_name,
            email=self.email,
            hashed_password=self.hashed_password,
        )
