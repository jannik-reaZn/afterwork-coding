from backend.common.domain.constants import EXCEPTION_CODES
from backend.common.domain.exceptions.base_exception import DomainBaseException
from backend.features.battleship.domain.models.cell import Cell

CELL_OUT_OF_BOUND_EXCEPTION_MESSAGE = (
    "Cell {cell} is out of bounds for board size {board_size}x{board_size}"
)


class CellOutOfBoundException(DomainBaseException):
    def __init__(self, cell: Cell, board_size: int) -> None:
        super().__init__(
            title="Cell out of bound exception",
            code=EXCEPTION_CODES.NOT_ACCEPTABLE,
            message=CELL_OUT_OF_BOUND_EXCEPTION_MESSAGE.format(cell=cell, board_size=board_size),
        )
