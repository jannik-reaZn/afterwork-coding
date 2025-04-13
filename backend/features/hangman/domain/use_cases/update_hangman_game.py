from backend.features.hangman.domain.models import HangmanGame


class GuessHangmanLetterUseCase:
    def __call__(self, hangman_status: HangmanGame, guessed_letter: str) -> HangmanGame:
        """
        Updates the state of the Hangman game based on the guessed letter.

        Args:
            hangman_status (HangmanGame): The current state of the Hangman game.
            guessed_letter (str): The letter guessed by the player.

        Returns:
            HangmanGame: The updated state of the Hangman game.
        """
        if self._is_game_lost(hangman_status):
            return hangman_status

        if guessed_letter not in hangman_status.guessed_letters:
            hangman_status.guessed_letters.append(guessed_letter)
            if guessed_letter not in hangman_status.random_word:
                hangman_status.total_tries -= 1

        if self._is_game_won(hangman_status):
            hangman_status.is_game_won_status = True

        return hangman_status

    def _is_game_won(self, hangman_status: HangmanGame) -> bool:
        """
        Determines if the Hangman game has been won.

        Args:
            hangman_status (HangmanGame): The current status of the Hangman game,
                including the random word to guess and the letters guessed so far.

        Returns:
            bool: True if all letters in the random word have been guessed, False otherwise.
        """
        return (
            True
            if set(hangman_status.random_word).issubset(set(hangman_status.guessed_letters))
            else False
        )

    def _is_game_lost(self, hangman_status: HangmanGame) -> bool:
        """
        Determines if the hangman game is lost.

        Args:
            hangman_status (HangmanGame): The current status of the hangman game,
                including the number of remaining tries.

        Returns:
            bool: True if the game is lost (i.e., no remaining tries), False otherwise.
        """
        return True if hangman_status.total_tries == 0 else False
