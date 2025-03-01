from sqlmodel import select

from backend.database import SessionDependency
from backend.features.auth.repositories.auth_repository import AuthRepository
from backend.features.user.repositories.sql.entities import UserSqlEntity


class AuthRepositorySQL(AuthRepository):
    def __init__(self, session: SessionDependency):
        self.session = session

    async def get_user_by_username(self, username: str) -> UserSqlEntity | None:
        statement = select(UserSqlEntity).where(UserSqlEntity.username == username)
        return self.session.exec(statement).first()
