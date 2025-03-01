from abc import ABC, abstractmethod

from backend.common.repository.base_repository import BaseRepository
from backend.features.user.domain.models import User, UserCreate


class UserRepository(BaseRepository, ABC):
    @abstractmethod
    def create(self, user: UserCreate) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: int) -> User:
        raise NotImplementedError
