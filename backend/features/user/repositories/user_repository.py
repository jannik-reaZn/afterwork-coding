from abc import ABC, abstractmethod

from backend.common.repository.base_repository import BaseRepository
from backend.features.user.domain.models import UserCreate
from backend.features.user.repositories.sql.entities import UserSqlEntity


class UserRepository(BaseRepository, ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> UserSqlEntity:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, username: str) -> UserSqlEntity:
        raise NotImplementedError
