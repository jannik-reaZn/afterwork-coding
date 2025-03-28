from typing import Protocol


class WordProviderInterface(Protocol):
    def get_random_word(self) -> str:
        """Return a random word from the word provider."""
        ...
