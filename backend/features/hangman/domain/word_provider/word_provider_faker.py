from typing import Callable

from faker import Faker

from backend.features.hangman.domain.word_provider.interface import WordProviderInterface


class WordProviderFaker(WordProviderInterface):
    """
    A class that provides random words using the Faker library.

    Attributes:
        language (str): The language code used to generate words.
        fake (Faker): An instance of the Faker class initialized with the specified language.
    """

    def __init__(self, language: str, mode: str):
        self.language = language
        self.mode = mode
        self.fake = Faker(language)

    def get_random_word(self) -> str:
        """
        Generates a random word using the Faker library and returns it in uppercase.

        Returns:
            str: A randomly generated word in uppercase.
        """
        match self.mode.value:
            case "word":
                return self.fake.word().upper()
            case "sentence":
                return "Dies ist ein Satz".upper()


def get_word_provider_factory() -> Callable[[str], WordProviderInterface]:
    """
    Creates a factory function for generating instances of WordProviderFaker.

    Returns:
        Callable[[str], WordProviderInterface]: A factory function that takes a
        language as input and returns an instance of WordProviderFaker configured
        for the specified language.
    """

    def factory(language: str, mode: str) -> WordProviderInterface:
        return WordProviderFaker(language=language, mode=mode)

    return factory
