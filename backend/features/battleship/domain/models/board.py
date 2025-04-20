from typing import Dict

from pydantic import Field

from backend.common.domain.models import DomainModel
from backend.features.battleship.domain.exceptions.cell_out_of_bound_exception import (
    CellOutOfBoundException,
)
from backend.features.battleship.domain.models.cell import Cell, CellState
from backend.features.battleship.domain.models.constants import (
    DEFAULT_BOARD_SIZE,
    MAXIMUM_BOARD_SIZE,
    MINIMUM_BOARD_SIZE,
)


class Board(DomainModel):
    size: int = Field(
        description="Size of the board",
        ge=MINIMUM_BOARD_SIZE,
        le=MAXIMUM_BOARD_SIZE,
        default=DEFAULT_BOARD_SIZE,
    )
    grid: Dict[Cell, CellState] = Field(default_factory=dict, examples=[{(1, 1): CellState.EMPTY}])

    def __init__(self, **data):
        super().__init__(**data)
        # Since the grid starts at (1, 1), one needs to iterate from 1 to size + 1
        for row in range(1, self.size + 1):
            for col in range(1, self.size + 1):
                self.grid[(col, row)] = CellState.EMPTY

    def is_within_bounds(self, cell: Cell) -> bool:
        """
        Determine if a given cell is within the boundaries of the board.

        Args:
            cell (Cell): A tuple representing the row and column indices of the cell.

        Returns:
            bool: True if the cell is within the board boundaries, False otherwise.
        """
        row, col = cell
        return 1 <= row <= self.size and 1 <= col <= self.size

    def get_cell_state(self, cell: Cell) -> CellState:
        """
        Retrieve the state of a specific cell on the board.

        Args:
            cell (Cell): The cell for which the state is to be retrieved.

        Returns:
            CellState: The state of the specified cell. Returns `CellState.EMPTY`
            if the cell is not explicitly set in the grid.
        """
        if not self.is_within_bounds(cell):
            raise CellOutOfBoundException(cell=cell, board_size=self.size)
        return self.grid.get(cell, CellState.EMPTY)

    def set_cell_state(self, cell: Cell, state: CellState) -> None:
        """
        Updates the state of a specific cell on the board.

        Args:
            cell (Cell): The cell to update.
            state (CellState): The new state to assign to the cell.
        """
        if not self.is_within_bounds(cell):
            raise CellOutOfBoundException(cell=cell, board_size=self.size)
        self.grid[cell] = state
