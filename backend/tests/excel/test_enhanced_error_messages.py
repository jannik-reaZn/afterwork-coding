import pytest

from backend.features.excel.domain.errors.example_model_error_mapper import ExampleModelErrorMapper
from backend.features.excel.domain.errors.row_validation_error import RowValidationError
from backend.features.excel.domain.model.example_model import ExampleModel
from backend.features.excel.domain.use_cases.excel_validator_use_case import ExcelValidationUseCase


def test_enhanced_error_messages():
    """Test that error messages include the actual input values."""

    # Setup with custom error mapper
    error_mapper = ExampleModelErrorMapper()
    validator = ExcelValidationUseCase[ExampleModel](model=ExampleModel, error_mapper=error_mapper)

    # Test data with various invalid values
    invalid_rows = [
        {
            "author": "John Doe",
            "description": "Test description",
            "code": "ABC123",  # Invalid: should be 4 digits
        },
        {
            "author": "",  # Invalid: missing/empty
            "description": "Another test",
            "code": "12345",  # Invalid: too long
        },
        {
            "author": "Jane Smith",
            "description": 123,  # Invalid: should be string
            "code": "1234",  # Valid
        },
    ]

    # Execute and expect validation error
    try:
        validator(invalid_rows)
        assert False, "Expected RowValidationError"
    except RowValidationError as e:
        # Check that error messages contain the actual input values
        error_messages = [err.message for err in e.errors]

        # Should contain the invalid code values in the error messages
        assert any(
            "ABC123" in msg for msg in error_messages
        ), "Should include invalid code 'ABC123'"
        assert any("12345" in msg for msg in error_messages), "Should include invalid code '12345'"
        assert any(
            "123" in msg for msg in error_messages
        ), "Should include invalid description '123'"

        # Test field-specific messages
        code_errors = [err for err in e.errors if err.field == "code"]
        assert any(
            "must be exactly 4 digits" in err.message for err in code_errors
        ), "Should have field-specific message for code field"

        print("Enhanced error messages:")
        for err in e.errors:
            print(f"Row {err.row_index}, Field {err.field}: {err.message}")


@pytest.mark.parametrize(
    "invalid_data,expected_field,expected_input_value,expected_message_part",
    [
        (
            {"author": "John", "description": "Test", "code": "ABC123"},
            "code",
            "ABC123",
            "must be exactly 4 digits",
        ),
        (
            {"author": "John", "description": "Test", "code": "12345"},
            "code",
            "12345",
            "must be exactly 4 digits",
        ),
        (
            {"author": "John", "description": "Test", "code": "12"},
            "code",
            "12",
            "must be exactly 4 digits",
        ),
        (
            {"author": "John", "description": 123, "code": "1234"},
            "description",
            "123",
            "must be a text value",
        ),
    ],
)
def test_enhanced_error_messages_parameterized(
    invalid_data: dict,
    expected_field: str,
    expected_input_value: str | None,
    expected_message_part: str,
):
    """Test specific error messages for individual validation failures."""

    # Setup with custom error mapper
    error_mapper = ExampleModelErrorMapper()
    validator = ExcelValidationUseCase[ExampleModel](model=ExampleModel, error_mapper=error_mapper)

    # Execute and expect validation error
    try:
        validator([invalid_data])
        assert False, "Expected RowValidationError"
    except RowValidationError as e:
        # Find the error for the expected field
        field_errors = [err for err in e.errors if err.field == expected_field]
        assert len(field_errors) > 0, f"Should have error for field '{expected_field}'"

        error = field_errors[0]

        # Check that the error message contains the expected parts
        assert (
            expected_message_part in error.message
        ), f"Message should contain '{expected_message_part}'"

        # Check input value is included if expected
        if expected_input_value is not None:
            assert (
                expected_input_value in error.message
            ), f"Message should contain input value '{expected_input_value}'"
