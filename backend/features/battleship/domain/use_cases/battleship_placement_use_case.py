from typing import List, Set

from backend.features.battleship.domain.models.board import Board
from backend.features.battleship.domain.models.cell import Cell, CellState


class BattleshipPlacementUseCase:
    def __init__(self, board: Board):
        self.board = board

    def __call__(self) -> bool:
        """
        Validates whether the placement of ships on the board is correct.

        Ships should:
        1. Form straight lines (either horizontally or vertically)
        2. Not touch each other (including diagonally)

        Returns:
            bool: True if all ship placements are valid, False otherwise
        """
        ship_cells = self._find_all_ship_cells()
        ships = self._identify_ships(ship_cells)

        for ship in ships:
            if not self._is_ship_straight(ship):
                return False

        return not self._are_ships_touching(ships)

    def _find_all_ship_cells(self) -> List[Cell]:
        """Find all cells that contain ships on the board"""
        ship_cells = []
        for row in range(1, self.board.size + 1):
            for col in range(1, self.board.size + 1):
                cell = (row, col)
                if self.board.get_cell_state(cell) == CellState.SHIP:
                    ship_cells.append(cell)
        return ship_cells

    def _identify_ships(self, ship_cells: List[Cell]) -> List[Set[Cell]]:
        """Group connected ship cells into distinct ships"""
        ships = []
        remaining_cells = set(ship_cells)

        while remaining_cells:
            current_ship = set()
            cell_queue = [remaining_cells.pop()]

            while cell_queue:
                current_cell = cell_queue.pop(0)
                current_ship.add(current_cell)

                # Check adjacent cells (horizontally and vertically)
                row, col = current_cell
                for adjacent_cell in [
                    (row + 1, col),
                    (row - 1, col),
                    (row, col + 1),
                    (row, col - 1),
                ]:
                    if adjacent_cell in remaining_cells:
                        remaining_cells.remove(adjacent_cell)
                        cell_queue.append(adjacent_cell)

            ships.append(current_ship)

        return ships

    def _is_ship_straight(self, ship_cells: Set[Cell]) -> bool:
        """Check if a ship forms a straight line (horizontally or vertically)"""
        if len(ship_cells) <= 1:
            return True

        # Extract rows and columns
        rows = {cell[0] for cell in ship_cells}
        cols = {cell[1] for cell in ship_cells}

        # Ship is straight if all cells share the same row or same column
        return len(rows) == 1 or len(cols) == 1

    def _are_ships_touching(self, ships: List[Set[Cell]]) -> bool:
        """Check if any ships are touching each other (including diagonally)"""
        # For each ship, create a set of "surrounding" cells to check
        for i, ship in enumerate(ships):
            ship_surroundings = set()

            # Get all surrounding cells for this ship in a 3x3 grid
            for cell in ship:
                row, col = cell
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        if (r, c) != cell and self.board.is_within_bounds((r, c)):
                            ship_surroundings.add((r, c))

            # Check if any other ship's cells are in the surroundings of this ship
            for j, other_ship in enumerate(ships):
                if i != j and any(cell in ship_surroundings for cell in other_ship):
                    return True

        return False
