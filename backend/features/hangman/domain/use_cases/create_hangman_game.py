from typing import Callable

from backend.features.hangman.domain.models import HangmanGame, HangmanLanguage, HangmanMode
from backend.features.hangman.domain.word_provider.interface import WordProviderInterface


class StartHangmanGameUseCase:
    def __init__(
        self, word_provider_factory: Callable[[HangmanLanguage, HangmanMode], WordProviderInterface]
    ):
        """
        Initializes the CreateHangmanGame use case.

        Args:
            word_provider_factory: A factory function that takes a language string and a HangmanMode
            and returns an instance of WordProviderInterface, used to provide words for the game.
        """
        self.word_provider_factory = word_provider_factory

    def __call__(
        self, total_tries: int, language: HangmanLanguage, mode: HangmanMode
    ) -> HangmanGame:
        """
        Creates a new HangmanGame instance with a random word and specified total tries.

        Args:
            total_tries (int): The total number of tries allowed for the game.
            language (HangmanLanguage): The language to be used for selecting the random word.
            mode (HangmanMode): The mode for the hangman game (word or sentence).

        Returns:
            HangmanGame: A new instance of the HangmanGame initialized with a random word,
            the specified total tries, an empty list of guessed letters, and a default
            game-won status of False.
        """
        word_provider = self.word_provider_factory(language, mode)
        random_word = word_provider.get_random_content()
        return HangmanGame(
            random_word=random_word,
            total_tries=total_tries,
            guessed_letters=[],
            is_game_won_status=False,
        )
