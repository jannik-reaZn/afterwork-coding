from enum import StrEnum

from pydantic import BaseModel, Field


class HangmanStatus(BaseModel):
    random_word: str
    total_tries: int = Field(
        ge=0,
        default=6,
        description="These are the total tries for the hangman game.",
    )
    guessed_letters: set[str]
    is_game_won_status: bool = False


class HangmanLanguages(StrEnum):
    ENGLISH = "en_US"
    GERMAN = "de_DE"
