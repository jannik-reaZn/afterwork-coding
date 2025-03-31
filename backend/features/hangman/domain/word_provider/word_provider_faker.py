from typing import Callable

from faker import Faker

from backend.features.hangman.domain.word_provider.interface import WordProviderInterface


class WordProviderFaker(WordProviderInterface):
    def __init__(self, language: str):
        self.language = language
        self.fake = Faker(language)

    def get_random_word(self) -> str:
        return self.fake.word().upper()


def get_word_provider_factory() -> Callable[[str], WordProviderInterface]:
    def factory(language: str) -> WordProviderInterface:
        return WordProviderFaker(language=language)

    return factory
