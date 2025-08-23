from typing import Generic, TypeVar

from pydantic import ValidationError

from backend.common.domain.models.domain_model import DomainModel
from backend.features.excel.domain.errors import DEFAULT_ERROR_CATALOG, ErrorMapper
from backend.features.excel.domain.errors.row_validation_error import RowValidationError

T = TypeVar("T", bound=DomainModel)


class ExcelValidationUseCase(Generic[T]):
    def __init__(
        self,
        model: type[T],
        *,
        start_row_index: int = 2,
        error_mapper: ErrorMapper | None = None,
    ):
        self.model = model
        self.start_row_index = start_row_index
        self.error_mapper = error_mapper or ErrorMapper(DEFAULT_ERROR_CATALOG)

    def _display_field_name(self, field_name: str | None) -> str | None:
        if field_name is None:
            return None
        mf = getattr(self.model, "model_fields", {}).get(field_name)
        return (getattr(mf, "alias", None) or field_name) if mf else field_name

    def __call__(self, rows: list[dict[str, object]]) -> list[T]:
        items: list[T] = []
        friendly_errors = []

        for i, raw in enumerate(rows):
            row_index = self.start_row_index + i
            try:
                item = self.model.model_validate(
                    {k.strip(): v for k, v in raw.items() if str(k).strip()}
                )
                items.append(item)
            except ValidationError as ve:
                for e in ve.errors():
                    loc = e.get("loc", [])
                    code = e.get("type", "invalid")
                    field = str(loc[0]) if loc else None
                    friendly_errors.append(
                        self.error_mapper.map(
                            row_index=row_index,
                            field=self._display_field_name(field),
                            code=code,
                            ctx=e.get("ctx"),
                            default_raw_msg=e.get("msg"),
                        )
                    )

        if friendly_errors:
            raise RowValidationError(friendly_errors)

        return items
