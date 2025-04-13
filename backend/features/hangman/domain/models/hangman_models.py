from typing import List

from pydantic import Field

from backend.common.domain.models import DomainModel
from backend.features.hangman.domain.constants import DEFAULT_HANGMAN_TOTAL_TRIES


class HangmanGame(DomainModel):
    random_word: str = Field(
        min_length=1,
        description="This is the random word for the hangman game.",
    )
    total_tries: int = Field(
        ge=0,
        default=DEFAULT_HANGMAN_TOTAL_TRIES,
        description="These are the total tries for the hangman game.",
    )
    guessed_letters: List[str] = Field(
        default=[],
        description="These are the letters guessed by the user.",
    )
    is_game_won_status: bool = Field(
        default=False,
        description="Indicates wether a game is won.",
    )
