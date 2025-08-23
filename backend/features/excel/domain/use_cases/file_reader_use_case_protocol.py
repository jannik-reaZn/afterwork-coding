from abc import abstractmethod
from typing import Protocol


class FileReaderUseCaseProtocol(Protocol):
    """Protocol defining the interface for file readers."""

    @abstractmethod
    def __call__(self, **kwargs) -> list[dict[str, object]]:
        """Read file and return structured data as a list of dictionaries."""
        ...
