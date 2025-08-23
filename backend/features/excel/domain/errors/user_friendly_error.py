from pydantic import Field

from backend.common.domain.models.domain_model import DomainModel


class UserFriendlyError(DomainModel):
    row_index: int = Field(
        title="Row Index",
        description="The 1-based row number in the Excel file where the validation error occurred."
        "This helps users locate the problematic data in their spreadsheet.",
        ge=1,
    )
    field: str | None = Field(
        title="Field Name",
        description="The name of the field that failed validation."
        "This corresponds to the pydantic model field name or alias."
        "Can be None if the error is not field-specific.",
        default=None,
    )
    code: str = Field(
        title="Error Code",
        description="Internal validation error code from Pydantic (e.g. 'missing', 'int_parsing').",
    )
    message: str = Field(
        title="User Message",
        description="A user friendly error message that explains what went wrong.",
    )
