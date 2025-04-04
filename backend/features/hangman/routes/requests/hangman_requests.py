from typing import List

from backend.common.domain.models import DomainModel


class HangmanRequest(DomainModel):
    random_word: str
    total_tries: int
    guessed_letters: List[str]
    is_game_won_status: bool
