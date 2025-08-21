# Catalog structure:
# {
#   "codes": { "<code>": "<message template>" },
#   "fields": {
#       "<model_field_or_alias>": { "<code>": "<message template>" }
#   },
#   "default": "<fallback message template>"
# }
from typing import Any, Mapping

from backend.common.domain.models.domain_model import DomainModel

ErrorCatalog = Mapping[str, Any]


class UserFriendlyError(DomainModel):
    row_index: int
    field: str | None
    code: str  # pydantic error "type", e.g. "string_pattern_mismatch"
    message: str  # mapped, user-facing message


class ErrorMapper:
    """Maps a raw Pydantic error to a user-friendly message."""

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
            # field-specific override first
            (self.catalog.get("fields", {}).get(field or "", {}) or {}).get(code)
            # then generic code-level message
            or self.catalog.get("codes", {}).get(code)
            # then global default
            or self.catalog.get("default")
            # last resort: fall back to pydantic's raw msg
            or default_raw_msg
            or "Invalid value."
        )
        # lightweight templating via str.format on ctx
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
