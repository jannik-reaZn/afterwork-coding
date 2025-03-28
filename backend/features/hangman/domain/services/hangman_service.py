from backend.features.hangman.domain.constants import DEFAULT_HANGMAN_TOTAL_TRIES
from backend.features.hangman.domain.models import HangmanStatus
from backend.features.hangman.domain.services.word_provider.interface import WordProviderInterface


class HangmanService:
    def __init__(self, word_provider: WordProviderInterface):
        self.word_provider: str = word_provider

    def start_game(self, total_tries: int = DEFAULT_HANGMAN_TOTAL_TRIES) -> HangmanStatus:
        random_word: str = self.word_provider.get_random_word()
        return HangmanStatus(
            random_word=random_word,
            total_tries=total_tries,
            guessed_letters=set(),
            is_game_won_status=False,
        )

    def update_game(self, hangman_status: HangmanStatus, guessed_letter: str):
        if self.is_game_lost(hangman_status):
            return hangman_status

        if guessed_letter not in hangman_status.guessed_letters:
            hangman_status.guessed_letters.add(guessed_letter)
            if guessed_letter not in hangman_status.random_word:
                hangman_status.total_tries -= 1

        if self.is_game_won(hangman_status):
            hangman_status.is_game_won_status = True

        return hangman_status

    def is_game_won(self, hangman_status: HangmanStatus) -> bool:
        return True if hangman_status.guessed_letters == set(hangman_status.random_word) else False

    def is_game_lost(self, hangman_status: HangmanStatus) -> bool:
        return True if hangman_status.total_tries == 0 else False
