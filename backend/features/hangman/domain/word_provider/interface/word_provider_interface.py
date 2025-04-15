from typing import Protocol


class WordProviderInterface(Protocol):
    def get_random_content(self) -> str:
        """Return random text content (word or sentence) based on the configured mode."""
        ...
