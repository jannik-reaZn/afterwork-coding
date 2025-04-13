from typing import Callable

from backend.features.hangman.domain.models import HangmanGame
from backend.features.hangman.domain.word_provider.interface import WordProviderInterface


class StartHangmanGameUseCase:
    def __init__(self, word_provider_factory: Callable[[str], WordProviderInterface]):
        """
        Initializes the CreateHangmanGame use case.

        Args:
            word_provider_factory: A factory function that takes a string and returns an instance
            of WordProviderInterface, used to provide words for the hangman game.
        """
        self.word_provider_factory = word_provider_factory

    def __call__(self, total_tries: int, language: str) -> HangmanGame:
        """
        Creates a new HangmanGame instance with a random word and specified total tries.

        Args:
            total_tries (int): The total number of tries allowed for the game.
            language (str): The language to be used for selecting the random word.

        Returns:
            HangmanGame: A new instance of the HangmanGame initialized with a random word,
            the specified total tries, an empty list of guessed letters, and a default
            game-won status of False.
        """
        word_provider = self.word_provider_factory(language)
        random_word = word_provider.get_random_word()
        return HangmanGame(
            random_word=random_word,
            total_tries=total_tries,
            guessed_letters=[],
            is_game_won_status=False,
        )
