from sqlmodel import select

from backend.database import SessionDep
from backend.features.auth.repositories.auth_repository import AuthRepository
from backend.features.user.repositories.entity.user_entity import User


class AuthRepositorySQL(AuthRepository):
    def __init__(self, session: SessionDep):
        self.session = session

    async def get_user_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()
