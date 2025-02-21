from abc import ABC, abstractmethod

from backend.features.user.repositories.sql.entities.user_entity import User


class AuthRepository(ABC):
    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        raise NotImplementedError
