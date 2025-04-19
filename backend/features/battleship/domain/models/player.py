from pydantic import Field

from backend.common.domain.models import DomainModel
from backend.features.battleship.domain.models.board import Board, CellState
from backend.features.battleship.domain.models.ship import Ship


class Player(DomainModel):
    player_id: str
    player_name: str = Field(description="Name of the player")
    board: Board = Field(default_factory=Board)
    ships: list[Ship] = Field(default_factory=list)

    def place_ship(self, ship: Ship) -> None:
        # check if ship placement is valid
        if not self.is_ship_placement_valid(ship):
            raise ValueError("Invalid ship placement.")

        self.ships.append(ship)
        for position in ship.get_ship_positions:
            self.board.set_cell_state(position, CellState.SHIP)

    def is_ship_placement_valid(self, ship: Ship) -> bool:
        # check if the ship can be placed on the board
        for position in ship.get_ship_positions:
            if self.board.get_cell_state(position) != CellState.EMPTY:
                return False
        return True
