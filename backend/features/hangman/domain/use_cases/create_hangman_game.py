from typing import Callable

from backend.features.hangman.domain.models import HangmanGame
from backend.features.hangman.domain.word_provider.interface import WordProviderInterface


class StartHangmanGameUseCase:
    def __init__(self, word_provider_factory: Callable[[str], WordProviderInterface]):
        self.word_provider_factory = word_provider_factory

    def __call__(self, total_tries: int, language: str) -> HangmanGame:
        word_provider = self.word_provider_factory(language)
        random_word = word_provider.get_random_word()
        return HangmanGame(
            random_word=random_word,
            total_tries=total_tries,
            guessed_letters=[],
            is_game_won_status=False,
        )
