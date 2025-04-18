from typing import List

from pydantic import Field

from backend.common.domain.models import DomainModel


class HangmanRequest(DomainModel):
    random_word: str = Field(description="The random word/sentence for the hangman game.")
    total_tries: int = Field(
        ge=0,
        description="The total tries for the hangman game.",
    )
    guessed_letters: List[str] = Field(
        description="The letters guessed by the user.",
    )
    is_game_won_status: bool = Field(
        description="Indicates whether a game is won.",
    )
