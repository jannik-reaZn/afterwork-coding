from __future__ import annotations

from enum import StrEnum, auto
from typing import Set

from pydantic import Field

from backend.common.domain.models import DomainModel
from backend.features.battleship.domain.models.board import Cell


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
        length = SHIP_LENGTHS.get(ship_type)
        if length is None:
            raise ValueError(f"Invalid ship type: {ship_type}")
        return length

    @classmethod
    def create_ship(
        cls, ship_type: ShipType, orientation: ShipOrientation, start_position: Cell
    ) -> Ship:
        return cls(
            ship_type=ship_type,
            length=cls.get_ship_length(ship_type),
            orientation=orientation,
            start_position=start_position,
        )

    def register_hit(self, cell: Cell) -> None:
        if cell not in self.hit_cells:
            self.hit_cells.add(cell)

    def is_ship_sunk(self) -> bool:
        return len(self.hit_cells) == self.length

    def are_all_ships_sunk(self, ships: list[Ship]) -> bool:
        return all(ship.is_ship_sunk() for ship in ships)
