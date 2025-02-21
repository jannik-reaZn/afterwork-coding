from abc import ABC, abstractmethod

from backend.common.repository.base_repository import BaseRepository
from backend.features.user.repositories.sql.entities.user_entity import User


class UserRepository(BaseRepository, ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        raise NotImplementedError

    def get_user(self, username: str) -> User:
        raise NotImplementedError


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
