from abc import ABC, abstractmethod
from typing import Any


class BaseRepository(ABC):
    @abstractmethod
    def create(self, create_tdo: Any):
        raise NotImplementedError
