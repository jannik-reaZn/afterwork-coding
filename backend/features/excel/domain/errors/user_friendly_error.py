from backend.common.domain.models.domain_model import DomainModel


class UserFriendlyError(DomainModel):
    row_index: int
    field: str | None
    code: str  # pydantic error "type", e.g. "string_pattern_mismatch"
    message: str  # mapped, user-facing message
