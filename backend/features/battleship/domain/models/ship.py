from __future__ import annotations

from enum import StrEnum, auto
from typing import Set

from pydantic import Field

from backend.common.domain.models import DomainModel
from backend.features.battleship.domain.models.cell import Cell


class ShipType(StrEnum):
    CARRIER = auto()
    BATTLESHIP = auto()
    CRUISER = auto()
    SUBMARINE = auto()
    DESTROYER = auto()


class ShipOrientation(StrEnum):
    HORIZONTAL = auto()
    VERTICAL = auto()


SHIP_LENGTHS = {
    ShipType.CARRIER: 5,
    ShipType.BATTLESHIP: 4,
    ShipType.CRUISER: 3,
    ShipType.SUBMARINE: 3,
    ShipType.DESTROYER: 2,
}


class Ship(DomainModel):
    ship_type: ShipType = Field(description="Type of the ship")
    length: int = Field(description="Length of the ship", ge=1, le=5)
    orientation: ShipOrientation = Field(
        description="Orientation of the ship", default=ShipOrientation.HORIZONTAL
    )
    start_position: Cell = Field(description="Start position of the ship on the board")
    hit_cells: Set[Cell] = Field(default_factory=set, description="Set of cells that have been hit")

    @property
    def get_ship_positions(self) -> list[Cell]:
        """
        Calculate and return the positions occupied by the ship on the grid.

        The positions are determined based on the ship's starting position,
        length, and orientation (horizontal or vertical).

        Returns:
            list[Cell]: A list of positions (row, column) occupied by the ship.
        """
        row, col = self.start_position
        positions = []

        for i in range(self.length):
            if self.orientation == ShipOrientation.HORIZONTAL:
                positions.append((row, col + i))
            else:
                positions.append((row + i, col))

        return positions

    @staticmethod
    def get_ship_length(ship_type: ShipType) -> int:
        """
        Retrieve the length of a ship based on its type.

        Args:
            ship_type (ShipType): The type of the ship for which the length is required.

        Returns:
            int: The length of the ship corresponding to the given type.
        """
        length = SHIP_LENGTHS.get(ship_type)
        if length is None:
            raise ValueError(f"Invalid ship type: {ship_type}")
        return length

    @classmethod
    def create_ship(
        cls, ship_type: ShipType, orientation: ShipOrientation, start_position: Cell
    ) -> Ship:
        """
        Creates a new Ship instance with the specified type, orientation, and starting position.

        Args:
            ship_type (ShipType): The type of the ship to be created.
            orientation (ShipOrientation): The orientation of the ship (horizontal or vertical).
            start_position (Cell): The starting position of the ship on the grid.

        Returns:
            Ship: A new instance of the Ship class with the specified attributes.
        """
        return cls(
            ship_type=ship_type,
            length=cls.get_ship_length(ship_type),
            orientation=orientation,
            start_position=start_position,
        )

    def register_hit(self, cell: Cell) -> None:
        """
        Registers a hit on the ship at the specified cell.

        Args:
            cell (Cell): The cell where the hit occurred.
        """
        if cell not in self.hit_cells:
            self.hit_cells.add(cell)

    def is_ship_sunk(self) -> bool:
        """
        Determines if the ship is sunk.

        A ship is considered sunk if the number of cells that have been hit
        is equal to the total length of the ship.

        Returns:
            bool: True if the ship is sunk, False otherwise.
        """
        return len(self.hit_cells) == self.length
