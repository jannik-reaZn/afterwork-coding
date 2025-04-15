import os
import random
from typing import Callable

from faker import Faker

from backend.features.hangman.domain.content_factory.interface import ContentFactoryInterface
from backend.features.hangman.domain.models import HangmanLanguage, HangmanMode


class TextContentFactory(ContentFactoryInterface):
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
                return self.choose_random_sentence_from_file()
            case _:
                raise ValueError(f"Unsupported mode: {self.mode}")

    def choose_random_sentence_from_file(self) -> str:
        sentences = []
        sentences_file = os.path.join(os.path.dirname(__file__), "german_sentences.txt")
        with open(sentences_file, "r") as file:
            for line in file:
                sentences.append(str(line).rstrip("\n"))
        return random.choice(sentences).upper()


def get_text_content_factory() -> Callable[[HangmanLanguage, HangmanMode], ContentFactoryInterface]:
    """
    Creates a factory function for generating instances of TextContentFactory.

    Returns:
        Callable[[str, HangmanMode], ContentFactoryInterface]: A factory function that takes a
        language string and a HangmanMode as input and returns an instance of TextContentFactory
        configured for the specified language and mode.
    """

    def factory(language: HangmanLanguage, mode: HangmanMode) -> ContentFactoryInterface:
        return TextContentFactory(language=language, mode=mode)

    return factory
