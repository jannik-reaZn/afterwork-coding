import pytest

from backend.features.hangman.domain.models import HangmanStatus
from backend.features.hangman.domain.use_cases import GuessHangmanLetterUseCase


@pytest.fixture
def guess_letter_use_case():
    return GuessHangmanLetterUseCase()


def test_correct_guess(guess_letter_use_case):
    total_tries = 5
    status = HangmanStatus(
        random_word="PYTHON", total_tries=total_tries, guessed_letters=[], is_game_won_status=False
    )

    updated = guess_letter_use_case(hangman_status=status, guessed_letter="P")

    assert "P" in updated.guessed_letters
    assert updated.total_tries == total_tries
    assert updated.is_game_won_status is False


def test_incorrect_guess(guess_letter_use_case):
    total_tries = 5
    status = HangmanStatus(
        random_word="PYTHON", total_tries=total_tries, guessed_letters=[], is_game_won_status=False
    )

    updated = guess_letter_use_case(hangman_status=status, guessed_letter="Z")

    assert "Z" in updated.guessed_letters
    assert updated.total_tries == total_tries - 1
    assert updated.is_game_won_status is False


def test_game_won(guess_letter_use_case):
    status = HangmanStatus(
        random_word="HI", total_tries=5, guessed_letters=["H"], is_game_won_status=False
    )

    updated = guess_letter_use_case(hangman_status=status, guessed_letter="I")

    assert "I" in updated.guessed_letters
    assert updated.is_game_won_status is True


def test_no_op_when_game_lost(guess_letter_use_case):
    status = HangmanStatus(
        random_word="HI", total_tries=0, guessed_letters=[], is_game_won_status=False
    )

    updated = guess_letter_use_case(hangman_status=status, guessed_letter="H")

    assert updated.total_tries == 0
    assert "H" not in updated.guessed_letters
    assert updated.is_game_won_status is False
