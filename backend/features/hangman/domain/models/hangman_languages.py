from enum import StrEnum
from typing import Dict, List

from pydantic import BaseModel


class HangmanLanguage(StrEnum):
    AMERICAN = "american"
    GERMAN = "german"


# Language-specific alphabets
LANGUAGE_ALPHABETS: Dict[HangmanLanguage, List[str]] = {
    HangmanLanguage.AMERICAN: list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    HangmanLanguage.GERMAN: list("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß"),
}


# Pydantic model for response
class HangmanAlphabet(BaseModel):
    alphabet: List[str]
