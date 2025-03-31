import pytest

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
    response = test_client.get("api/hangman/start", params={"tries": 7, "language": "american"})

    assert response.status_code == 200
    data = response.json()

    assert data["random_word"] == "STATICWORD"
    assert data["total_tries"] == 7
    assert data["guessed_letters"] == []
    assert data["is_game_won_status"] is False


def test_guess_letter_correct(test_client):
    # Start a game first
    start_response = test_client.get("api/hangman/start", params={"tries": 5, "language": "en_US"})
    game_state = start_response.json()

    # Guess a letter that exists
    guess_response = test_client.post(f"api/hangman/guess/S", json=game_state)

    assert guess_response.status_code == 200
    data = guess_response.json()

    assert "S" in data["guessed_letters"]
    assert data["total_tries"] == 5  # no penalty
    assert data["is_game_won_status"] is False


def test_guess_letter_incorrect(test_client):
    # Start a game first
    start_response = test_client.get("api/hangman/start", params={"tries": 5, "language": "en_US"})
    game_state = start_response.json()

    # Guess a letter that does not exist
    guess_response = test_client.post(f"api/hangman/guess/Z", json=game_state)

    assert guess_response.status_code == 200
    data = guess_response.json()

    assert "Z" in data["guessed_letters"]
    assert data["total_tries"] == 4  # penalty for wrong guess
    assert data["is_game_won_status"] is False


def test_game_win(test_client):
    # Setup game with only one letter missing
    state = {
        "random_word": "HI",
        "total_tries": 5,
        "guessed_letters": ["H"],
        "is_game_won_status": False,
    }

    guess_response = test_client.post("api/hangman/guess/I", json=state)

    assert guess_response.status_code == 200
    data = guess_response.json()

    assert "I" in data["guessed_letters"]
    assert data["is_game_won_status"] is True
