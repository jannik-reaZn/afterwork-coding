import pytest

from backend.features.battleship.domain.exceptions.cell_out_of_bound_exception import (
    CellOutOfBoundException,
)
from backend.features.battleship.domain.models.board import Board, CellState
from backend.features.battleship.domain.models.constants import (
    DEFAULT_BOARD_SIZE,
    MAXIMUM_BOARD_SIZE,
    MINIMUM_BOARD_SIZE,
)


@pytest.mark.parametrize(
    "board_size",
    [MINIMUM_BOARD_SIZE, DEFAULT_BOARD_SIZE, MAXIMUM_BOARD_SIZE],
)
def test_board_initialization2(board_size):
    """Test that the board is initialized with the correct size and all cells are EMPTY."""
    board = Board(size=board_size)

    # Check that the board size is set correctly
    assert board.size == board_size

    # Check that all cells are initialized to EMPTY
    for row in range(1, board_size + 1):
        for col in range(1, board_size + 1):
            assert board.grid[(col, row)] == CellState.EMPTY


def test_board_initialization_default_size():
    """Test that the board is initialized with the default size when no size is provided."""
    board = Board()

    # Check that the board size is set to the default size
    assert board.size == DEFAULT_BOARD_SIZE

    # Check that all cells are initialized to EMPTY
    for row in range(1, DEFAULT_BOARD_SIZE + 1):
        for col in range(1, DEFAULT_BOARD_SIZE + 1):
            assert board.grid[(col, row)] == CellState.EMPTY


@pytest.mark.parametrize(
    "board_size, cell, expected_result",
    [
        (DEFAULT_BOARD_SIZE, (1, 1), True),  # Cell at the top-left corner
        (
            DEFAULT_BOARD_SIZE,
            (DEFAULT_BOARD_SIZE, DEFAULT_BOARD_SIZE),
            True,
        ),  # Cell at the bottom-right corner
        (DEFAULT_BOARD_SIZE, (0, 1), False),  # Cell outside the left boundary
        (DEFAULT_BOARD_SIZE, (1, 0), False),  # Cell outside the top boundary
        (DEFAULT_BOARD_SIZE, (DEFAULT_BOARD_SIZE + 1, 1), False),  # Cell outside the right boundary
        (
            DEFAULT_BOARD_SIZE,
            (1, DEFAULT_BOARD_SIZE + 1),
            False,
        ),  # Cell outside the bottom boundary
    ],
)
def test_is_within_bounds(board_size, cell, expected_result):
    """Test the is_within_bounds method with various cells and board sizes."""
    board = Board(size=board_size)
    assert board.is_within_bounds(cell) == expected_result


@pytest.mark.parametrize(
    "board_size, cell, expected_state",
    [
        (DEFAULT_BOARD_SIZE, (1, 1), CellState.EMPTY),  # Cell at the top-left corner
        (
            DEFAULT_BOARD_SIZE,
            (DEFAULT_BOARD_SIZE, DEFAULT_BOARD_SIZE),
            CellState.EMPTY,
        ),  # Bottom-right corner
    ],
)
def test_get_cell_state_within_bounds(board_size, cell, expected_state):
    """Test get_cell_state for cells within bounds."""
    board = Board(size=board_size)
    assert board.get_cell_state(cell) == expected_state


@pytest.mark.parametrize(
    "board_size, cell",
    [
        (DEFAULT_BOARD_SIZE, (0, 1)),  # Cell outside the left boundary
        (DEFAULT_BOARD_SIZE, (1, 0)),  # Cell outside the top boundary
        (DEFAULT_BOARD_SIZE, (DEFAULT_BOARD_SIZE + 1, 1)),  # Cell outside the right boundary
        (DEFAULT_BOARD_SIZE, (1, DEFAULT_BOARD_SIZE + 1)),  # Cell outside the bottom boundary
    ],
)
def test_get_cell_state_out_of_bounds(board_size, cell):
    """Test get_cell_state raises CellOutOfBoundException for cells out of bounds."""
    board = Board(size=board_size)
    with pytest.raises(CellOutOfBoundException):
        board.get_cell_state(cell)


@pytest.mark.parametrize(
    "board_size, cell, state",
    [
        (DEFAULT_BOARD_SIZE, (1, 1), CellState.HIT),  # Top-left corner
        (
            DEFAULT_BOARD_SIZE,
            (DEFAULT_BOARD_SIZE, DEFAULT_BOARD_SIZE),
            CellState.MISS,
        ),  # Bottom-right corner
    ],
)
def test_set_cell_state_within_bounds(board_size, cell, state):
    """Test set_cell_state for cells within bounds."""
    board = Board(size=board_size)
    board.set_cell_state(cell, state)
    assert board.grid[cell] == state


@pytest.mark.parametrize(
    "board_size, cell, state",
    [
        (DEFAULT_BOARD_SIZE, (0, 1), CellState.HIT),  # Cell outside the left boundary
        (DEFAULT_BOARD_SIZE, (1, 0), CellState.MISS),  # Cell outside the top boundary
        (DEFAULT_BOARD_SIZE, (DEFAULT_BOARD_SIZE + 1, 1), CellState.HIT),  # Outside right boundary
        (
            DEFAULT_BOARD_SIZE,
            (1, DEFAULT_BOARD_SIZE + 1),
            CellState.MISS,
        ),  # Outside bottom boundary
    ],
)
def test_set_cell_state_out_of_bounds(board_size, cell, state):
    """Test set_cell_state raises CellOutOfBoundException for cells out of bounds."""
    board = Board(size=board_size)
    with pytest.raises(CellOutOfBoundException):
        board.set_cell_state(cell, state)
