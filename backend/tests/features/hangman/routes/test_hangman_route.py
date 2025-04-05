import pytest

from backend.features.hangman.domain.models import HangmanLanguage
from backend.features.hangman.domain.word_provider import (
    WordProviderStatic,
    get_word_provider_factory,
)
from backend.features.hangman.domain.word_provider.interface import WordProviderInterface
from backend.main import app


@pytest.fixture(autouse=True)
def override_word_provider():
    def static_factory(_: str) -> WordProviderInterface:
        return WordProviderStatic("STATICWORD")

    app.dependency_overrides[get_word_provider_factory] = lambda: static_factory
    yield
    app.dependency_overrides.clear()


def test_start_game_endpoint(test_client):
    response = test_client.get(
        "api/hangman/start", params={"tries": 7, "language": HangmanLanguage.AMERICAN}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["randomWord"] == "STATICWORD"
    assert data["totalTries"] == 7
    assert data["guessedLetters"] == []
    assert data["isGameWonStatus"] is False


def test_guess_letter_correct(test_client):
    # Start a game first
    start_response = test_client.get(
        "api/hangman/start", params={"tries": 5, "language": HangmanLanguage.AMERICAN}
    )
    game_state = start_response.json()

    # Guess a letter that exists
    guess_response = test_client.post(f"api/hangman/guess/S", json=game_state)

    assert guess_response.status_code == 200
    data = guess_response.json()

    assert "S" in data["guessedLetters"]
    assert data["totalTries"] == 5  # no penalty
    assert data["isGameWonStatus"] is False


def test_guess_letter_incorrect(test_client):
    # Start a game first
    start_response = test_client.get(
        "api/hangman/start", params={"tries": 5, "language": HangmanLanguage.AMERICAN}
    )
    game_state = start_response.json()

    # Guess a letter that does not exist
    guess_response = test_client.post(f"api/hangman/guess/Z", json=game_state)

    assert guess_response.status_code == 200
    data = guess_response.json()

    assert "Z" in data["guessedLetters"]
    assert data["totalTries"] == 4  # penalty for wrong guess
    assert data["isGameWonStatus"] is False


def test_game_win(test_client):
    # Setup game with only one letter missing
    state = {
        "randomWord": "HI",
        "totalTries": 5,
        "guessedLetters": ["H"],
        "isGameWonStatus": False,
    }

    guess_response = test_client.post("api/hangman/guess/I", json=state)

    assert guess_response.status_code == 200
    data = guess_response.json()

    assert "I" in data["guessedLetters"]
    assert data["isGameWonStatus"] is True
