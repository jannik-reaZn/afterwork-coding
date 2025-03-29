from typing import Callable

from backend.features.hangman.domain.constants import DEFAULT_HANGMAN_TOTAL_TRIES
from backend.features.hangman.domain.models import HangmanLanguages, HangmanStatus
from backend.features.hangman.domain.services.word_provider import WordProviderFaker
from backend.features.hangman.domain.services.word_provider.interface import WordProviderInterface


class HangmanService:
    def __init__(self, word_provider_factory: Callable[[str], WordProviderInterface]):
        self.word_provider_factory = word_provider_factory

    def start_game(
        self,
        total_tries: int = DEFAULT_HANGMAN_TOTAL_TRIES,
        language: str = HangmanLanguages.AMERICAN.value,
    ) -> HangmanStatus:
        word_provider = self.word_provider_factory(language)
        random_word = word_provider.get_random_word()
        return HangmanStatus(
            random_word=random_word,
            total_tries=total_tries,
            guessed_letters=[],
            is_game_won_status=False,
        )

    def guess_letter(self, hangman_status: HangmanStatus, guessed_letter: str) -> HangmanStatus:
        if self.is_game_lost(hangman_status):
            return hangman_status

        if guessed_letter not in hangman_status.guessed_letters:
            hangman_status.guessed_letters.append(guessed_letter)
            if guessed_letter not in hangman_status.random_word:
                hangman_status.total_tries -= 1

        if self.is_game_won(hangman_status):
            hangman_status.is_game_won_status = True

        return hangman_status

    def is_game_won(self, hangman_status: HangmanStatus) -> bool:
        return (
            True
            if set(hangman_status.random_word).issubset(set(hangman_status.guessed_letters))
            else False
        )

    def is_game_lost(self, hangman_status: HangmanStatus) -> bool:
        return True if hangman_status.total_tries == 0 else False


def get_hangman_service() -> HangmanService:
    def word_provider_factory(language: str) -> WordProviderInterface:
        return WordProviderFaker(language=language)

    return HangmanService(word_provider_factory=word_provider_factory)
