from enum import StrEnum, auto


class HangmanMode(StrEnum):
    """
    Enum representing the available modes for the Hangman game.

    Attributes:
        WORD: Represents the mode where only one WORD is guessed.
        SENTENCE: Represents the mode where a german SENTENCE is guessed.
    """

    WORD = auto()
    SENTENCE = auto()
