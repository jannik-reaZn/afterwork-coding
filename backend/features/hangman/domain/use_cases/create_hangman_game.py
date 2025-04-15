from typing import Callable

from backend.features.hangman.domain.content_factory.interface import ContentFactoryInterface
from backend.features.hangman.domain.models import HangmanGame, HangmanLanguage, HangmanMode


class StartHangmanGameUseCase:
    def __init__(
        self, content_factory: Callable[[HangmanLanguage, HangmanMode], ContentFactoryInterface]
    ):
        """
        Initializes the CreateHangmanGame use case.

        Args:
            content_factory: A factory function that takes a language string and a HangmanMode
            and returns an instance of ContentFactoryInterface, used to provide words for the game.
        """
        self.content_factory = content_factory

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
        content_factory = self.content_factory(language, mode)
        random_word = content_factory.get_random_content()
        return HangmanGame(
            random_word=random_word,
            total_tries=total_tries,
            guessed_letters=[],
            is_game_won_status=False,
        )
