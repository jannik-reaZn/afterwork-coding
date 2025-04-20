from pydantic import Field

from backend.common.domain.models import DomainModel
from backend.features.battleship.domain.models.board import Board
from backend.features.battleship.domain.models.cell import CellState
from backend.features.battleship.domain.models.ship import Ship


class Player(DomainModel):
    player_id: str
    player_name: str = Field(description="Name of the player")
    board: Board = Field(default_factory=Board)
    ships: list[Ship] = Field(default_factory=list)

    def place_ship(self, ship: Ship) -> None:
        """
        Places a ship on the player's board.

        This method validates the ship's placement and, if valid, adds the ship
        to the player's list of ships and updates the board to reflect the ship's
        position.

        Args:
            ship (Ship): The ship to be placed on the board.

        Raises:
            ValueError: If the ship's placement is invalid.
        """
        if not self.is_ship_placement_valid(ship):
            raise ValueError("Invalid ship placement.")

        self.ships.append(ship)
        for position in ship.get_ship_positions:
            self.board.set_cell_state(position, CellState.SHIP)

    def is_ship_placement_valid(self, ship: Ship) -> bool:
        """
        Checks if the placement of a given ship on the board is valid.

        This method verifies whether all the positions that the ship would occupy
        on the board are currently empty. If any position is already occupied, the
        placement is considered invalid.

        Args:
            ship (Ship): The ship object to be placed on the board.

        Returns:
            bool: True if the ship can be placed on the board without conflicts,
                  False otherwise.
        """
        for position in ship.get_ship_positions:
            if self.board.get_cell_state(position) != CellState.EMPTY:
                return False
        return True

    def are_all_ships_sunk(self, ships: list[Ship]) -> bool:
        """
        Determines if all ships in the provided list are sunk.

        Args:
            ships (list[Ship]): A list of Ship objects to check.

        Returns:
            bool: True if all ships in the list are sunk, False otherwise.
        """
        return all(ship.is_ship_sunk() for ship in ships)
