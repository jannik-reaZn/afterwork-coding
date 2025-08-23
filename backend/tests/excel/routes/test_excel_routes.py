import ast
import io
from collections.abc import Callable
from typing import Any

import pytest
from openpyxl import Workbook

from backend.features.excel.domain.model.example_model import ExampleModel


@pytest.fixture
def make_example_model():
    def make(author="User1", description="Some description", code="1234"):
        return ExampleModel(author=author, description=description, code=code)

    return make


def _xlsx_bytes_with_rows(rows: list[list[Any]], headers: list[str]) -> bytes:
    wb = Workbook()
    ws = wb.active
    if ws is None:
        ws = wb.create_sheet()
    ws.append(headers)
    for r in rows:
        ws.append(r)

    bio = io.BytesIO()
    wb.save(bio)
    return bio.getvalue()


@pytest.fixture
def example_content() -> bytes:
    headers: list[str] = ["author", "description", "code"]
    rows: list[list[Any]] = [["John Doe", "Something", "1999"]]

    return _xlsx_bytes_with_rows(
        rows=rows,
        headers=headers,
    )


@pytest.fixture
def make_excel_file() -> Callable[[bytes], dict[str, tuple[str, bytes, str]]]:
    def make(file: bytes) -> dict[str, tuple[str, bytes, str]]:
        return {
            "file": (
                "file.xlsx",
                file,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        }

    return make


@pytest.fixture
def invalid_code_content() -> bytes:
    headers: list[str] = ["author", "description", "code"]
    rows: list[list[Any]] = [
        ["John Doe", "Something", "12345"],  # Too long (5 digits instead of 4)
        ["Jane Smith", "Another", "ABC1"],  # Contains letters
        ["Bob Wilson", "Test", "12"],  # Too short (2 digits instead of 4)
    ]

    return _xlsx_bytes_with_rows(
        rows=rows,
        headers=headers,
    )


def test_excel_route(test_client, make_excel_file, example_content: bytes):
    # GIVEN
    file = make_excel_file(example_content)

    # WHEN
    response = test_client.post("/api/excel/", files=file)
    response_data = response.json()

    # THEN
    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]["author"] == "John Doe"
    assert response_data[0]["description"] == "Something"


def test_excel_route_invalid_code_pattern(
    test_client, make_excel_file, invalid_code_content: bytes
):
    # GIVEN
    file = make_excel_file(invalid_code_content)

    # WHEN
    response = test_client.post("/api/excel/", files=file)
    response_data = response.json()

    # THEN
    assert response.status_code == 422
    assert "description" in response_data

    # Extract errors from the description field
    description = response_data["description"]

    errors = ast.literal_eval(description)

    # Should have 3 validation errors (one for each invalid row)
    assert len(errors) == 3

    # Check that all errors are for the 'code' field with pattern mismatch
    for error in errors:
        assert error["field"] == "code"
        assert error["code"] == "string_pattern_mismatch"
        # assert error["message"] == "Invalid format for '12345'. Expected format not met."

    # Check specific row indices (starting from row 2 as per start_row_index)
    assert errors[0]["row_index"] == 2  # First data row
    assert errors[1]["row_index"] == 3  # Second data row
    assert errors[2]["row_index"] == 4  # Third data row
