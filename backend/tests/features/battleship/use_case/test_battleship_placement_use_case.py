import pytest

from backend.features.battleship.domain.models.board import Board
from backend.features.battleship.domain.models.cell import CellState
from backend.features.battleship.domain.use_cases.battleship_placement_use_case import (
    BattleshipPlacementUseCase,
)


@pytest.fixture
def make_battleship_board():
    return Board(size=10)


@pytest.fixture
def make_battleship_board_with_placements(make_battleship_board):
    board = make_battleship_board
    board.set_cell_state(cell=(1, 1), state=CellState.SHIP)
    board.set_cell_state(cell=(1, 2), state=CellState.SHIP)
    return board


@pytest.fixture
def make_battleship_board_with_wrong_placements(make_battleship_board):
    board = make_battleship_board
    board.set_cell_state(cell=(1, 1), state=CellState.SHIP)
    board.set_cell_state(cell=(1, 2), state=CellState.SHIP)
    board.set_cell_state(cell=(2, 2), state=CellState.SHIP)
    return board


@pytest.fixture
def make_battleship_board_with_edge_placements(make_battleship_board):
    """Board with ships placed at the edges"""
    board = make_battleship_board
    # Ship at top edge
    board.set_cell_state(cell=(1, 1), state=CellState.SHIP)
    board.set_cell_state(cell=(1, 2), state=CellState.SHIP)
    board.set_cell_state(cell=(1, 3), state=CellState.SHIP)

    # Ship at right edge
    board.set_cell_state(cell=(3, 10), state=CellState.SHIP)
    board.set_cell_state(cell=(4, 10), state=CellState.SHIP)

    # Ship at bottom edge
    board.set_cell_state(cell=(10, 6), state=CellState.SHIP)
    board.set_cell_state(cell=(10, 7), state=CellState.SHIP)
    board.set_cell_state(cell=(10, 8), state=CellState.SHIP)

    # Ship at left edge
    board.set_cell_state(cell=(7, 1), state=CellState.SHIP)
    board.set_cell_state(cell=(8, 1), state=CellState.SHIP)

    return board


@pytest.fixture
def make_battleship_board_with_diagonal_ship(make_battleship_board):
    """Board with a ship placed diagonally (invalid)"""
    board = make_battleship_board
    board.set_cell_state(cell=(5, 5), state=CellState.SHIP)
    board.set_cell_state(cell=(6, 6), state=CellState.SHIP)
    board.set_cell_state(cell=(7, 7), state=CellState.SHIP)
    return board


@pytest.fixture
def make_battleship_board_with_l_shape(make_battleship_board):
    """Board with a ship placed in an L-shape (invalid)"""
    board = make_battleship_board
    board.set_cell_state(cell=(3, 3), state=CellState.SHIP)
    board.set_cell_state(cell=(3, 4), state=CellState.SHIP)
    board.set_cell_state(cell=(4, 4), state=CellState.SHIP)
    return board


@pytest.fixture
def make_battleship_board_with_touching_ships(make_battleship_board):
    """Board with two ships touching diagonally (invalid)"""
    board = make_battleship_board
    # First ship - horizontal
    board.set_cell_state(cell=(2, 2), state=CellState.SHIP)
    board.set_cell_state(cell=(2, 3), state=CellState.SHIP)

    # Second ship - vertical - touching at the corner
    board.set_cell_state(cell=(3, 4), state=CellState.SHIP)
    board.set_cell_state(cell=(4, 4), state=CellState.SHIP)
    return board


@pytest.fixture
def make_battleship_board_with_adjacent_ships(make_battleship_board):
    """Board with two ships touching side by side (invalid)"""
    board = make_battleship_board
    # First ship - horizontal
    board.set_cell_state(cell=(2, 2), state=CellState.SHIP)
    board.set_cell_state(cell=(2, 3), state=CellState.SHIP)

    # Second ship - horizontal - adjacent
    board.set_cell_state(cell=(3, 2), state=CellState.SHIP)
    board.set_cell_state(cell=(3, 3), state=CellState.SHIP)
    return board


@pytest.fixture
def make_battleship_board_with_multiple_valid_ships(make_battleship_board):
    """Board with multiple valid ships properly spaced"""
    board = make_battleship_board
    # Ship 1 - horizontal at top
    board.set_cell_state(cell=(1, 1), state=CellState.SHIP)
    board.set_cell_state(cell=(1, 2), state=CellState.SHIP)
    board.set_cell_state(cell=(1, 3), state=CellState.SHIP)

    # Ship 2 - vertical in middle
    board.set_cell_state(cell=(4, 5), state=CellState.SHIP)
    board.set_cell_state(cell=(5, 5), state=CellState.SHIP)
    board.set_cell_state(cell=(6, 5), state=CellState.SHIP)
    board.set_cell_state(cell=(7, 5), state=CellState.SHIP)

    # Ship 3 - horizontal at bottom
    board.set_cell_state(cell=(10, 7), state=CellState.SHIP)
    board.set_cell_state(cell=(10, 8), state=CellState.SHIP)
    return board


@pytest.fixture
def make_battleship_board_with_single_cell_ships(make_battleship_board):
    """Board with single cell ships that are properly spaced"""
    board = make_battleship_board
    board.set_cell_state(cell=(2, 2), state=CellState.SHIP)
    board.set_cell_state(cell=(2, 4), state=CellState.SHIP)
    board.set_cell_state(cell=(4, 2), state=CellState.SHIP)
    board.set_cell_state(cell=(4, 4), state=CellState.SHIP)
    return board


@pytest.fixture
def make_battleship_board_corner_case(make_battleship_board):
    """Board with ships in the corners"""
    board = make_battleship_board
    # Top-left corner
    board.set_cell_state(cell=(1, 1), state=CellState.SHIP)
    board.set_cell_state(cell=(1, 2), state=CellState.SHIP)

    # Top-right corner
    board.set_cell_state(cell=(1, 9), state=CellState.SHIP)
    board.set_cell_state(cell=(1, 10), state=CellState.SHIP)

    # Bottom-left corner
    board.set_cell_state(cell=(9, 1), state=CellState.SHIP)
    board.set_cell_state(cell=(10, 1), state=CellState.SHIP)

    # Bottom-right corner
    board.set_cell_state(cell=(10, 9), state=CellState.SHIP)
    board.set_cell_state(cell=(10, 10), state=CellState.SHIP)

    return board


@pytest.fixture
def make_battleship_board_with_zigzag(make_battleship_board):
    """Board with a ship in zigzag form (invalid)"""
    board = make_battleship_board
    board.set_cell_state(cell=(5, 5), state=CellState.SHIP)
    board.set_cell_state(cell=(5, 6), state=CellState.SHIP)
    board.set_cell_state(cell=(6, 6), state=CellState.SHIP)
    board.set_cell_state(cell=(6, 7), state=CellState.SHIP)
    return board


def test_battleship_placement_use_case(make_battleship_board_with_placements):
    """Test ships placed correctly on the board"""
    board = make_battleship_board_with_placements
    validated_placement = BattleshipPlacementUseCase(board)()
    assert validated_placement is True


def test_battleship_placement_use_case_with_wrong_placements(
    make_battleship_board_with_wrong_placements,
):
    """Test ships placed incorrectly on the board"""
    board = make_battleship_board_with_wrong_placements
    validated_placement = BattleshipPlacementUseCase(board)()
    assert validated_placement is False


def test_edge_placements(make_battleship_board_with_edge_placements):
    """Test ships placed at the edges of the board"""
    board = make_battleship_board_with_edge_placements
    validated_placement = BattleshipPlacementUseCase(board)()
    assert validated_placement is True


def test_diagonal_ship(make_battleship_board_with_diagonal_ship):
    """Test a ship placed diagonally which should be invalid"""
    board = make_battleship_board_with_diagonal_ship
    validated_placement = BattleshipPlacementUseCase(board)()
    assert validated_placement is False


def test_l_shape_ship(make_battleship_board_with_l_shape):
    """Test a ship placed in L-shape which should be invalid"""
    board = make_battleship_board_with_l_shape
    validated_placement = BattleshipPlacementUseCase(board)()
    assert validated_placement is False


def test_ships_touching_diagonally(make_battleship_board_with_touching_ships):
    """Test ships touching diagonally which should be invalid"""
    board = make_battleship_board_with_touching_ships
    validated_placement = BattleshipPlacementUseCase(board)()
    assert validated_placement is False


def test_ships_adjacent(make_battleship_board_with_adjacent_ships):
    """Test ships placed side-by-side which should be invalid"""
    board = make_battleship_board_with_adjacent_ships
    validated_placement = BattleshipPlacementUseCase(board)()
    assert validated_placement is False


def test_multiple_valid_ships(make_battleship_board_with_multiple_valid_ships):
    """Test multiple ships with valid placement"""
    board = make_battleship_board_with_multiple_valid_ships
    validated_placement = BattleshipPlacementUseCase(board)()
    assert validated_placement is True


def test_single_cell_ships(make_battleship_board_with_single_cell_ships):
    """Test placement of single-cell ships"""
    board = make_battleship_board_with_single_cell_ships
    validated_placement = BattleshipPlacementUseCase(board)()
    assert validated_placement is True


def test_corner_case_ships(make_battleship_board_corner_case):
    """Test ships placed in the corners of the board"""
    board = make_battleship_board_corner_case
    validated_placement = BattleshipPlacementUseCase(board)()
    assert validated_placement is True


def test_zigzag_ship(make_battleship_board_with_zigzag):
    """Test a ship in zigzag shape which should be invalid"""
    board = make_battleship_board_with_zigzag
    validated_placement = BattleshipPlacementUseCase(board)()
    assert validated_placement is False
