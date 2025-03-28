from typing import Set

from pydantic import BaseModel


class HangmanRequest(BaseModel):
    random_word: str
    total_tries: int
    guessed_letters: Set[str]
    is_game_won_status: bool
