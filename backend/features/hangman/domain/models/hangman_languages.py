from enum import StrEnum, auto
from typing import Dict, List

from backend.common.domain.models import DomainModel


class HangmanLanguage(StrEnum):
    AMERICAN = auto()
    GERMAN = auto()


# Language-specific alphabets
LANGUAGE_ALPHABETS: Dict[HangmanLanguage, List[str]] = {
    HangmanLanguage.AMERICAN: list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    HangmanLanguage.GERMAN: list("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß"),
}


# Pydantic model for response
class HangmanAlphabet(DomainModel):
    alphabet: List[str]
