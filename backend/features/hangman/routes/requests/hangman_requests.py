from typing import List

from pydantic import BaseModel


class HangmanRequest(BaseModel):
    random_word: str
    total_tries: int
    guessed_letters: List[str]
    is_game_won_status: bool
