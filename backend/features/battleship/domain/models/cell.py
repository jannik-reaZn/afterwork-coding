from enum import StrEnum, auto
from typing import Tuple


class CellState(StrEnum):
    EMPTY = auto()
    SHIP = auto()
    HIT = auto()
    MISS = auto()


type Cell = Tuple[int, int]
