from enum import StrEnum
from typing import Dict, List

from backend.common.domain.models import DomainModel


class HangmanLanguage(StrEnum):
    AMERICAN = "american"
    GERMAN = "german"


# Language-specific alphabets
LANGUAGE_ALPHABETS: Dict[HangmanLanguage, List[str]] = {
    HangmanLanguage.AMERICAN: list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    HangmanLanguage.GERMAN: list("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß"),
}


# Pydantic model for response
class HangmanAlphabet(DomainModel):
    alphabet: List[str]
