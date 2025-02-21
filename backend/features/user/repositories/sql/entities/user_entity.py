from typing import Optional

from passlib.context import CryptContext
from sqlmodel import Field

from backend.common.repository.entities.base_sql_entity import BaseSqlEntity

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserSqlEntity(BaseSqlEntity, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    full_name: str | None = None
    email: str
    hashed_password: str

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)
