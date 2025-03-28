import pytest

from backend.features.hangman.domain.constants import DEFAULT_HANGMAN_TOTAL_TRIES
from backend.features.hangman.domain.services.hangman_service import HangmanService
from backend.features.hangman.domain.services.word_provider import WordProviderStatic


@pytest.fixture
def word_provider_static():
    return WordProviderStatic("hangman")


@pytest.fixture
def hangman_game(word_provider_static):
    return HangmanService(word_provider=word_provider_static)


class TestHangmanInit:
    @pytest.fixture(autouse=True)
    def _start_hangman_game(self, word_provider_static, hangman_game):
        self.word_provider_static = word_provider_static
        self.hangman = hangman_game

    def test_init_with_valid_word_provider(self):
        assert self.hangman.word_provider == self.word_provider_static


class TestHangmanStartGame:
    @pytest.fixture(autouse=True)
    def _start_hangman_game(self):
        self.word_provider_static = WordProviderStatic("hangman")
        self.hangman = HangmanService(word_provider=self.word_provider_static)

    def test_start_game_with_default_tries(self):
        hangman_status = self.hangman.start_game()

        # Assert
        assert hangman_status.random_word == "hangman"
        assert hangman_status.total_tries == DEFAULT_HANGMAN_TOTAL_TRIES
        assert hangman_status.guessed_letters == set()
        assert hangman_status.is_game_won_status is False


class TestHangmanGameLogic:
    @pytest.fixture(autouse=True)
    def _start_hangman_game(self, hangman_game):
        self.total_tries = DEFAULT_HANGMAN_TOTAL_TRIES
        self.hangman = hangman_game
        self.initial_status = hangman_game.start_game(total_tries=self.total_tries)

    def test_guess_letter_correct_guess(self):
        updated_status = self.hangman.guess_letter(self.initial_status, "h")

        # Assert
        assert updated_status.total_tries == self.total_tries
        assert "h" in updated_status.guessed_letters
        assert updated_status.is_game_won_status is False

    def test_guess_letter_incorrect_guess(self):
        updated_status = self.hangman.guess_letter(self.initial_status, "x")

        # Assert
        assert updated_status.total_tries == self.total_tries - 1
        assert "x" in updated_status.guessed_letters
        assert updated_status.is_game_won_status is False

    def test_is_game_won(self):
        status = self.initial_status

        # Pretend that all letters were guessed correctly
        for letter in "hangman":
            status = self.hangman.guess_letter(status, letter)

        # Act & Assert
        assert self.hangman.is_game_won(status) is True
        assert status.is_game_won_status is True

    @pytest.mark.parametrize(
        "guessed_letters, expected",
        [
            (["h", "a", "n", "g", "m"], False),
            (["h", "a", "n", "g", "m", "x"], False),
            (["x", "y", "k", "l", "w", "d"], True),
        ],
    )
    def test_is_game_lost(self, guessed_letters, expected):
        status = self.initial_status

        for letter in guessed_letters:
            status = self.hangman.guess_letter(status, letter)

        assert self.hangman.is_game_lost(status) == expected
