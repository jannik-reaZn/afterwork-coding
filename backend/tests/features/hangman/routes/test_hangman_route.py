import pytest

from backend.features.hangman.domain.content_factory import (
    WordProviderStatic,
    get_text_content_factory,
)
from backend.features.hangman.domain.content_factory.interface import ContentFactoryInterface
from backend.features.hangman.domain.models import LANGUAGE_ALPHABETS, HangmanLanguage, HangmanMode
from backend.main import app

HANGMAN_ROUTE = "api/hangman"


@pytest.fixture(autouse=True)
def override_word_provider():
    def static_factory(_: str, __: HangmanMode) -> ContentFactoryInterface:
        return WordProviderStatic(word="STATICWORD")

    app.dependency_overrides[get_text_content_factory] = lambda: static_factory
    yield
    app.dependency_overrides.clear()


def test_get_settings(test_client):
    response = test_client.get(f"{HANGMAN_ROUTE}/settings")
    data = response.json()

    assert response.status_code == 200
    assert data["languages"] == ["american", "german"]
    assert data["tries"] == [6, 7, 8, 9]


@pytest.mark.parametrize(
    "language, alphabet, layout_hints",
    [
        (
            HangmanLanguage.AMERICAN,
            LANGUAGE_ALPHABETS[HangmanLanguage.AMERICAN],
            ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"],
        ),
        (
            HangmanLanguage.GERMAN,
            LANGUAGE_ALPHABETS[HangmanLanguage.GERMAN],
            ["QWERTZUIOPÜß", "ASDFGHJKLÖÄ", "YXCVBNM"],
        ),
    ],
)
def test_get_alphabet(test_client, language, alphabet, layout_hints):
    response = test_client.get(f"{HANGMAN_ROUTE}/alphabet", params={"language": language})
    data = response.json()

    assert response.status_code == 200
    assert data["alphabet"] == alphabet
    assert data["layoutHints"] == layout_hints


def test_start_game(test_client):
    response = test_client.get(
        f"{HANGMAN_ROUTE}/start",
        params={"tries": 7, "language": HangmanLanguage.AMERICAN, "mode": HangmanMode.WORD},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["randomWord"] == "STATICWORD"
    assert data["totalTries"] == 7
    assert data["guessedLetters"] == []
    assert data["isGameWonStatus"] is False


def test_guess_letter_correct(test_client):
    # Start a game first
    start_response = test_client.get(
        f"{HANGMAN_ROUTE}/start",
        params={"tries": 5, "language": HangmanLanguage.AMERICAN, "mode": HangmanMode.WORD},
    )
    game_state = start_response.json()

    # Guess a letter that exists
    guess_response = test_client.post(f"{HANGMAN_ROUTE}/guess/S", json=game_state)
    data = guess_response.json()

    assert guess_response.status_code == 200
    assert "S" in data["guessedLetters"]
    assert data["totalTries"] == 5  # no penalty
    assert data["isGameWonStatus"] is False


def test_guess_letter_incorrect(test_client):
    # Start a game first
    start_response = test_client.get(
        f"{HANGMAN_ROUTE}/start",
        params={"tries": 5, "language": HangmanLanguage.AMERICAN, "mode": HangmanMode.WORD},
    )
    game_state = start_response.json()

    # Guess a letter that does not exist
    guess_response = test_client.post(f"{HANGMAN_ROUTE}/guess/Z", json=game_state)
    data = guess_response.json()

    assert guess_response.status_code == 200
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

    guess_response = test_client.post(f"{HANGMAN_ROUTE}/guess/I", json=state)
    data = guess_response.json()

    assert guess_response.status_code == 200
    assert "I" in data["guessedLetters"]
    assert data["isGameWonStatus"] is True
