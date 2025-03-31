import pytest

from backend.features.hangman.domain.constants import DEFAULT_HANGMAN_TOTAL_TRIES
from backend.features.hangman.domain.use_cases import StartHangmanGameUseCase
from backend.features.hangman.domain.word_provider import WordProviderStatic
from backend.features.hangman.domain.word_provider.interface import WordProviderInterface


@pytest.fixture
def word_provider_static():
    return WordProviderStatic("hangman")


@pytest.fixture
def word_provider_factory(word_provider_static):
    def factory(_: str) -> WordProviderInterface:
        return word_provider_static

    return factory


@pytest.fixture
def start_game_use_case(word_provider_factory):
    return StartHangmanGameUseCase(word_provider_factory=word_provider_factory)


def test_start_game_with_defaults(start_game_use_case):
    status = start_game_use_case(total_tries=DEFAULT_HANGMAN_TOTAL_TRIES, language="en")

    assert status.random_word == "hangman"
    assert status.total_tries == DEFAULT_HANGMAN_TOTAL_TRIES
    assert status.guessed_letters == []
    assert status.is_game_won_status is False
