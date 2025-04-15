from typing import Callable

from faker import Faker

from backend.features.hangman.domain.models import HangmanLanguage, HangmanMode
from backend.features.hangman.domain.word_provider.interface import WordProviderInterface


class TextContentFactory(WordProviderInterface):
    """
    A class that provides random text content (words or sentences) using the Faker library.

    Attributes:
        language (str): The language code used to generate content.
        mode (HangmanMode): The mode determining whether to generate words or sentences.
        fake (Faker): An instance of the Faker class initialized with the specified language.
    """

    def __init__(self, language: str, mode: HangmanMode):
        self.language = language
        self.mode = mode
        self.fake = Faker(language)

    def get_random_content(self) -> str:
        """
        Generates random text content based on the specified mode using the Faker library.

        Returns:
            str: A randomly generated word or sentence in uppercase.

        Raises:
            ValueError: If an unsupported mode is provided.
        """
        match self.mode.value:
            case HangmanMode.WORD.value:
                return self.fake.word().upper()
            case HangmanMode.SENTENCE.value:
                return "Dies ist ein Satz".upper()
            case _:
                raise ValueError(f"Unsupported mode: {self.mode}")


def get_text_content_factory() -> Callable[[HangmanLanguage, HangmanMode], WordProviderInterface]:
    """
    Creates a factory function for generating instances of TextContentFactory.

    Returns:
        Callable[[str, HangmanMode], WordProviderInterface]: A factory function that takes a
        language string and a HangmanMode as input and returns an instance of TextContentFactory
        configured for the specified language and mode.
    """

    def factory(language: HangmanLanguage, mode: HangmanMode) -> WordProviderInterface:
        return TextContentFactory(language=language, mode=mode)

    return factory
