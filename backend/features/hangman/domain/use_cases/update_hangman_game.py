from backend.features.hangman.domain.models import HangmanStatus


class GuessHangmanLetterUseCase:
    def __call__(self, hangman_status: HangmanStatus, guessed_letter: str) -> HangmanStatus:
        if self._is_game_lost(hangman_status):
            return hangman_status

        if guessed_letter not in hangman_status.guessed_letters:
            hangman_status.guessed_letters.append(guessed_letter)
            if guessed_letter not in hangman_status.random_word:
                hangman_status.total_tries -= 1

        if self._is_game_won(hangman_status):
            hangman_status.is_game_won_status = True

        return hangman_status

    def _is_game_won(self, hangman_status: HangmanStatus) -> bool:
        return (
            True
            if set(hangman_status.random_word).issubset(set(hangman_status.guessed_letters))
            else False
        )

    def _is_game_lost(self, hangman_status: HangmanStatus) -> bool:
        return True if hangman_status.total_tries == 0 else False
