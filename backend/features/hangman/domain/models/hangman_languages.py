from enum import StrEnum, auto
from typing import Dict, List

from backend.common.domain.models import DomainModel


class HangmanLanguage(StrEnum):
    """
    Enum representing the available languages for the Hangman game.

    Attributes:
        AMERICAN: Represents the American English language.
        GERMAN: Represents the German language.
    """

    AMERICAN = auto()
    GERMAN = auto()


# Mapping between each HangmanLanguage to its corresponding list of alphabet characters.
LANGUAGE_ALPHABETS: Dict[HangmanLanguage, List[str]] = {
    HangmanLanguage.AMERICAN: list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    HangmanLanguage.GERMAN: list("ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß"),
}


class HangmanAlphabet(DomainModel):
    """
    Represents the alphabet used in the Hangman game.

    Attributes:
        alphabet (List[str]): A list of characters representing the alphabet available for the
        Hangman game.
    """

    alphabet: List[str]
