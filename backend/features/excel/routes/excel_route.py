from fastapi import APIRouter, HTTPException

from backend.common.route.enums.api_routes import ApiRoutes
from backend.features.excel.domain.errors.row_validation_error import RowValidationError
from backend.features.excel.routes.dependencies import ExcelReaderDep, ExcelValidatorDep

router = APIRouter(prefix=f"/{ApiRoutes.EXCEL.value}")


@router.post("/")
async def validate_excel_file(reader: ExcelReaderDep, validator: ExcelValidatorDep):
    rows = reader()
    try:
        items = validator(rows)
        return items
    except RowValidationError as e:
        raise HTTPException(status_code=422, detail=[err.model_dump() for err in e.errors])
