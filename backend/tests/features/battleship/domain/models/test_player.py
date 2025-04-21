from unittest.mock import MagicMock

import pytest

from backend.features.battleship.domain.models.board import Board
from backend.features.battleship.domain.models.cell import CellState
from backend.features.battleship.domain.models.player import Player
from backend.features.battleship.domain.models.ship import Ship


@pytest.fixture
def mock_board():
    board = MagicMock(spec=Board)
    board.get_cell_state.return_value = CellState.EMPTY
    return board


@pytest.fixture
def mock_ship():
    ship = MagicMock(spec=Ship)
    ship.get_ship_positions = [(0, 0), (0, 1), (0, 2)]
    return ship


@pytest.fixture
def player(mock_board):
    return Player(player_id="1", player_name="Test Player", board=mock_board)


def test_place_ship_valid_placement(player, mock_ship):
    # Act
    player.place_ship(mock_ship)

    # Assert
    assert mock_ship in player.ships
    for position in mock_ship.get_ship_positions:
        player.board.set_cell_state.assert_any_call(position, CellState.SHIP)


def test_place_ship_invalid_placement(player, mock_ship):
    # Arrange
    player.board.get_cell_state.side_effect = lambda pos: (
        CellState.SHIP if pos == (0, 1) else CellState.EMPTY
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid ship placement."):
        player.place_ship(mock_ship)

    assert mock_ship not in player.ships
    player.board.set_cell_state.assert_not_called()


def test_is_ship_placement_valid_all_positions_empty(player, mock_ship):
    # Act
    result = player.is_ship_placement_valid(mock_ship)

    # Assert
    assert result is True
    for position in mock_ship.get_ship_positions:
        player.board.get_cell_state.assert_any_call(position)


def test_is_ship_placement_valid_some_positions_occupied(player, mock_ship):
    # Arrange
    player.board.get_cell_state.side_effect = lambda pos: (
        CellState.SHIP if pos == (0, 1) else CellState.EMPTY
    )

    # Act
    result = player.is_ship_placement_valid(mock_ship)

    # Assert
    assert result is False


def test_are_all_ships_sunk_all_sunk(player):
    # Arrange
    mock_ship_1 = MagicMock(spec=Ship)
    mock_ship_1.is_ship_sunk.return_value = True
    mock_ship_2 = MagicMock(spec=Ship)
    mock_ship_2.is_ship_sunk.return_value = True
    ships = [mock_ship_1, mock_ship_2]

    # Act
    result = player.are_all_ships_sunk(ships)

    # Assert
    assert result is True
    mock_ship_1.is_ship_sunk.assert_called_once()
    mock_ship_2.is_ship_sunk.assert_called_once()


def test_are_all_ships_sunk_some_not_sunk(player):
    # Arrange
    mock_ship_1 = MagicMock(spec=Ship)
    mock_ship_1.is_ship_sunk.return_value = True
    mock_ship_2 = MagicMock(spec=Ship)
    mock_ship_2.is_ship_sunk.return_value = False
    ships = [mock_ship_1, mock_ship_2]

    # Act
    result = player.are_all_ships_sunk(ships)

    # Assert
    assert result is False
    mock_ship_1.is_ship_sunk.assert_called_once()
    mock_ship_2.is_ship_sunk.assert_called_once()


def test_are_all_ships_sunk_no_ships(player):
    # Arrange
    ships = []

    # Act
    result = player.are_all_ships_sunk(ships)

    # Assert
    assert result is True
