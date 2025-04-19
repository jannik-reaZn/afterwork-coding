from enum import StrEnum, auto
from typing import Dict, Tuple

from pydantic import Field

from backend.common.domain.models import DomainModel
from backend.features.battleship.domain.models.constants import (
    DEFAULT_BOARD_SIZE,
    MAXIMUM_BOARD_SIZE,
    MINIMUM_BOARD_SIZE,
)


class CellState(StrEnum):
    EMPTY = auto()
    SHIP = auto()
    HIT = auto()
    MISS = auto()


type Cell = Tuple[int, int]


class Board(DomainModel):
    size: int = Field(
        description="Size of the board",
        ge=MINIMUM_BOARD_SIZE,
        le=MAXIMUM_BOARD_SIZE,
        default=DEFAULT_BOARD_SIZE,
    )
    grid: Dict[Cell, CellState] = Field(default_factory=dict, examples=[{(1, 1): CellState.EMPTY}])

    def __init__(self):
        self._initialize_empty_board()

    def _initialize_empty_board(self):
        # Since the grid starts at (1, 1), one needs to iterate from 1 to size + 1
        for row in range(1, self.size + 1):
            for col in range(1, self.size + 1):
                self.grid[(col, row)] = CellState.EMPTY

    def get_cell_state(self, cell: Cell) -> CellState:
        return self.grid.get(cell, CellState.EMPTY)

    def set_cell_state(self, cell: Cell, state: CellState):
        if cell in self.grid:
            self.grid[cell] = state
        else:
            raise ValueError(f"Cell {cell} is out of bounds.")
