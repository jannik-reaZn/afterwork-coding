from abc import ABC, abstractmethod

from backend.common.repository.base_repository import BaseRepository
from backend.features.user.repositories.sql.entities.user_entity import UserSqlEntity


class UserRepository(BaseRepository, ABC):
    @abstractmethod
    def create_user(self, user: UserSqlEntity) -> UserSqlEntity:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, username: str) -> UserSqlEntity:
        raise NotImplementedError
