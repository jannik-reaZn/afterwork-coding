from pydantic import BaseModel


class HangmanStatus(BaseModel):
    random_word: str
    total_tries: int
    guessed_letters: set[str]
