# Catalog structure:
# {
#   "codes": { "<code>": "<message template>" },
#   "fields": {
#       "<model_field_or_alias>": { "<code>": "<message template>" }
#   },
#   "default": "<fallback message template>"
# }
from typing import Any

from backend.common.domain.models.domain_model import DomainModel
from backend.features.excel.domain.errors.error_catalog import ErrorCatalog


class UserFriendlyError(DomainModel):
    row_index: int
    field: str | None
    code: str  # pydantic error "type", e.g. "string_pattern_mismatch"
    message: str  # mapped, user-facing message


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
    ) -> UserFriendlyError:
        ctx = ctx or {}
        msg = (
            self.catalog.resolve(field=field, code=code)
            or self.catalog.default
            or default_raw_msg
            or "Invalid value."
        )
        try:
            msg = msg.format(**ctx)
        except Exception:
            pass
        return UserFriendlyError(
            row_index=row_index,
            field=field,
            code=code,
            message=msg,
        )
