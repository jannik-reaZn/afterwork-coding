from typing import Any

from backend.features.excel.domain.errors import ErrorCatalog
from backend.features.excel.domain.errors.user_friendly_error import UserFriendlyError


class ErrorMapper:
    """
    Thin mapper that uses an ErrorCatalog to produce user-friendly messages.
    """

    def __init__(self, catalog: ErrorCatalog):
        self.catalog = catalog

    def map(
        self,
        *,
        row_index: int,
        field: str | None,
        code: str,
        ctx: dict[str, Any] | None = None,
        default_raw_msg: str | None = None,
        input_value: Any = None,
    ) -> UserFriendlyError:
        ctx = ctx or {}

        # Add the input value to context if provided
        if input_value is not None:
            ctx["input_value"] = input_value

        msg = (
            self.catalog.resolve(field=field, code=code)
            or self.catalog.default
            or default_raw_msg
            or "Invalid value."
        )
        try:
            msg = msg.format(**ctx)
        except Exception:
            pass  # Use the constructed message from above instead

        return UserFriendlyError(
            row_index=row_index,
            field=field,
            code=code,
            message=msg,
        )
