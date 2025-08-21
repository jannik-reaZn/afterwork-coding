from typing import Annotated

from fastapi import Depends, File, UploadFile

from backend.features.excel.domain.model import ExampleModel
from backend.features.excel.domain.use_cases import ExcelReaderUseCase, ExcelValidationUseCase


# Reader dependency: reads bytes in __init__
async def get_excel_reader(
    file: UploadFile = File(...),
) -> ExcelReaderUseCase:
    content = await file.read()
    return ExcelReaderUseCase(file_bytes=content, header_row=1)


# Validator dependency: inject the model (generic)
def get_excel_validator() -> ExcelValidationUseCase[ExampleModel]:
    return ExcelValidationUseCase[ExampleModel](model=ExampleModel)


ReaderDep = Annotated[ExcelReaderUseCase, Depends(get_excel_reader)]
ValidatorDep = Annotated[ExcelValidationUseCase[ExampleModel], Depends(get_excel_validator)]
