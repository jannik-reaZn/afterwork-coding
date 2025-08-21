from typing import Sequence

from backend.features.excel.domain.errors.user_friendly_error import UserFriendlyError


class RowValidationError(Exception):
    def __init__(self, errors: Sequence[UserFriendlyError]):
        self.errors = list(errors)
        super().__init__("Row validation failed")
