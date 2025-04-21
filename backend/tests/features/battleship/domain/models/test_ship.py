import pytest

from backend.features.battleship.domain.models.ship import Ship, ShipOrientation, ShipType


@pytest.mark.parametrize(
    "ship_type, orientation, start_position, expected_length",
    [
        (ShipType.CARRIER, ShipOrientation.HORIZONTAL, (0, 0), 5),
        (ShipType.BATTLESHIP, ShipOrientation.VERTICAL, (1, 1), 4),
        (ShipType.CRUISER, ShipOrientation.HORIZONTAL, (2, 2), 3),
        (ShipType.SUBMARINE, ShipOrientation.VERTICAL, (3, 3), 3),
        (ShipType.DESTROYER, ShipOrientation.HORIZONTAL, (4, 4), 2),
    ],
)
def test_create_ship(ship_type, orientation, start_position, expected_length):
    ship = Ship.create_ship(ship_type, orientation, start_position)

    assert ship.ship_type == ship_type
    assert ship.orientation == orientation
    assert ship.start_position == start_position
    assert ship.length == expected_length


@pytest.mark.parametrize(
    "ship_type, expected_length",
    [
        (ShipType.CARRIER, 5),
        (ShipType.BATTLESHIP, 4),
        (ShipType.CRUISER, 3),
        (ShipType.SUBMARINE, 3),
        (ShipType.DESTROYER, 2),
    ],
)
def test_get_ship_length_valid(ship_type, expected_length):
    assert Ship.get_ship_length(ship_type) == expected_length


def test_get_ship_length_invalid():
    with pytest.raises(ValueError, match="Invalid ship type: INVALID_SHIP"):
        Ship.get_ship_length("INVALID_SHIP")  # pyright: ignore


@pytest.mark.parametrize(
    "ship_type, orientation, start_position, expected_positions",
    [
        (
            ShipType.CARRIER,
            ShipOrientation.HORIZONTAL,
            (0, 0),
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
        ),
        (ShipType.BATTLESHIP, ShipOrientation.VERTICAL, (1, 1), [(1, 1), (2, 1), (3, 1), (4, 1)]),
        (ShipType.CRUISER, ShipOrientation.HORIZONTAL, (2, 2), [(2, 2), (2, 3), (2, 4)]),
        (ShipType.SUBMARINE, ShipOrientation.VERTICAL, (3, 3), [(3, 3), (4, 3), (5, 3)]),
        (ShipType.DESTROYER, ShipOrientation.HORIZONTAL, (4, 4), [(4, 4), (4, 5)]),
    ],
)
def test_get_ship_positions(ship_type, orientation, start_position, expected_positions):
    ship = Ship.create_ship(ship_type, orientation, start_position)
    assert ship.get_ship_positions == expected_positions


@pytest.mark.parametrize(
    "ship_type, orientation, start_position, hit_cells, hit_cell, expected_hit_cells",
    [
        (
            ShipType.CARRIER,
            ShipOrientation.HORIZONTAL,
            (0, 0),
            {(0, 1), (0, 2)},
            (0, 3),
            {(0, 1), (0, 2), (0, 3)},
        ),
        (
            ShipType.BATTLESHIP,
            ShipOrientation.VERTICAL,
            (1, 1),
            {(2, 1)},
            (3, 1),
            {(2, 1), (3, 1)},
        ),
        (
            ShipType.DESTROYER,
            ShipOrientation.HORIZONTAL,
            (4, 4),
            set(),
            (4, 5),
            {(4, 5)},
        ),
    ],
)
def test_register_hit(
    ship_type, orientation, start_position, hit_cells, hit_cell, expected_hit_cells
):
    ship = Ship.create_ship(ship_type, orientation, start_position)
    ship.hit_cells = hit_cells

    ship.register_hit(hit_cell)

    assert ship.hit_cells == expected_hit_cells


@pytest.mark.parametrize(
    "ship_type, orientation, start_position, hit_cells, expected_result",
    [
        (
            ShipType.CARRIER,
            ShipOrientation.HORIZONTAL,
            (0, 0),
            {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)},
            True,
        ),
        (ShipType.BATTLESHIP, ShipOrientation.VERTICAL, (1, 1), {(1, 1), (2, 1), (3, 1)}, False),
        (ShipType.DESTROYER, ShipOrientation.HORIZONTAL, (4, 4), set(), False),
    ],
)
def test_is_ship_sunk(ship_type, orientation, start_position, hit_cells, expected_result):
    ship = Ship.create_ship(ship_type, orientation, start_position)
    ship.hit_cells = hit_cells

    assert ship.is_ship_sunk() == expected_result
