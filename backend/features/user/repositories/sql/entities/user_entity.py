from typing import Optional

from passlib.context import CryptContext
from sqlmodel import Field

from backend.common.repository.entities.base_sql_entity import BaseSqlEntity
from backend.features.user.domain.models import User, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserSqlEntity(BaseSqlEntity, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(min_length=1, unique=True)
    full_name: str | None = None
    email: str = Field(min_length=1)
    hashed_password: str = Field(min_length=1)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    def to_domain(self) -> User:
        return User(
            **dict(
                id=self.id,
                username=self.username,
                full_name=self.full_name,
                email=self.email,
                hashed_password=self.hashed_password,
            )
        )

    @staticmethod
    def from_create_model(user_update_dto: UserCreate) -> "UserSqlEntity":
        return UserSqlEntity(**dict(user_update_dto.model_dump()))
