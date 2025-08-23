from typing import Annotated

from fastapi import Depends, File, UploadFile

from backend.features.excel.domain.errors.default_error_catalog import DEFAULT_ERROR_CATALOG
from backend.features.excel.domain.errors.error_mapper import ErrorMapper
from backend.features.excel.domain.model import ExampleModel
from backend.features.excel.domain.use_cases import ExcelReaderUseCase, ExcelValidationUseCase


async def get_excel_reader(
    file: UploadFile = File(...),
) -> ExcelReaderUseCase:
    content = await file.read()
    return ExcelReaderUseCase(file_bytes=content, header_row=1)


def get_excel_validator() -> ExcelValidationUseCase[ExampleModel]:
    mapper = ErrorMapper(DEFAULT_ERROR_CATALOG)
    return ExcelValidationUseCase[ExampleModel](model=ExampleModel, error_mapper=mapper)


ExcelReaderDep = Annotated[ExcelReaderUseCase, Depends(get_excel_reader)]
ExcelValidatorDep = Annotated[ExcelValidationUseCase[ExampleModel], Depends(get_excel_validator)]
