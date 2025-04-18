import pytest

from backend.features.hangman.domain.constants import DEFAULT_HANGMAN_TOTAL_TRIES
from backend.features.hangman.domain.content_factory import TextContentFactoryStatic
from backend.features.hangman.domain.content_factory.interface import ContentFactoryInterface
from backend.features.hangman.domain.models import HangmanMode
from backend.features.hangman.domain.use_cases import StartHangmanGameUseCase


@pytest.fixture
def word_provider_static():
    return TextContentFactoryStatic(text_content="hangman")


@pytest.fixture
def content_factory(word_provider_static):
    def factory(_: str, __: HangmanMode) -> ContentFactoryInterface:
        return word_provider_static

    return factory


@pytest.fixture
def start_game_use_case(content_factory):
    return StartHangmanGameUseCase(content_factory=content_factory)


def test_start_game_with_defaults(start_game_use_case):
    status = start_game_use_case(
        total_tries=DEFAULT_HANGMAN_TOTAL_TRIES, language="en", mode="word"
    )

    assert status.random_word == "hangman"
    assert status.total_tries == DEFAULT_HANGMAN_TOTAL_TRIES
    assert status.guessed_letters == []
    assert status.is_game_won_status is False
