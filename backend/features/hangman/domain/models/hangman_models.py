from enum import StrEnum

from pydantic import BaseModel, Field

from backend.features.hangman.domain.constants import DEFAULT_HANGMAN_TOTAL_TRIES


class HangmanStatus(BaseModel):
    random_word: str
    total_tries: int = Field(
        ge=0,
        default=DEFAULT_HANGMAN_TOTAL_TRIES,
        description="These are the total tries for the hangman game.",
    )
    guessed_letters: set[str]
    is_game_won_status: bool = False


class HangmanLanguages(StrEnum):
    ENGLISH = "en_US"
    GERMAN = "de_DE"
