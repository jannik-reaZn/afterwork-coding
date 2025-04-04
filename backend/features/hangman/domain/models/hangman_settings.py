from typing import List

from pydantic import BaseModel, Field

from backend.features.hangman.domain.constants import (
    DEFAULT_HANGMAN_TOTAL_TRIES,
    MAX_HANGMAN_TOTAL_TRIES,
)
from backend.features.hangman.domain.models import HangmanLanguage


class HangmanSettings(BaseModel):
    languages: List[HangmanLanguage] = Field(
        default=list(HangmanLanguage),
        description="Possible languages to choose from",
    )
    tries: List[int] = Field(
        default=range(DEFAULT_HANGMAN_TOTAL_TRIES, MAX_HANGMAN_TOTAL_TRIES + 1),
        description="List of tries to choose from",
    )
