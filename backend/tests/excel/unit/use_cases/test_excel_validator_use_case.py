from typing import cast

import pytest
from pydantic import Field

from backend.common.domain.models.domain_model import DomainModel
from backend.features.excel.domain.errors import DEFAULT_ERROR_CATALOG, ErrorMapper
from backend.features.excel.domain.errors.example_model_error_mapper import ExampleModelErrorMapper
from backend.features.excel.domain.errors.row_validation_error import RowValidationError
from backend.features.excel.domain.model.example_model import ExampleModel
from backend.features.excel.domain.use_cases.excel_validator_use_case import ExcelValidationUseCase


# Test models for different validation scenarios
class SimpleTestModel(DomainModel):
    name: str = Field()
    age: int = Field()


class OptionalFieldsModel(DomainModel):
    required_field: str = Field()
    optional_field: str | None = Field(default=None)


class ValidationRulesModel(DomainModel):
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")
    score: int = Field(ge=0, le=100)
    status: str = Field(min_length=3, max_length=10)


class AliasedFieldsModel(DomainModel):
    user_name: str = Field(alias="userName")
    user_email: str = Field(alias="userEmail")


@pytest.fixture
def valid_simple_rows() -> list[dict[str, object]]:
    """Create valid rows for SimpleTestModel."""
    return [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
        {"name": "Charlie", "age": 35},
    ]


@pytest.fixture
def invalid_simple_rows() -> list[dict[str, object]]:
    """Create invalid rows for SimpleTestModel."""
    return [
        {"name": "Alice", "age": "not_a_number"},  # Invalid age
        {"name": "", "age": 30},  # Valid
        {"age": 25},  # Missing name
        {"name": "Dave", "age": -5},  # Valid
    ]


@pytest.fixture
def mixed_simple_rows() -> list[dict[str, object]]:
    """Create a mix of valid and invalid rows."""
    return [
        {"name": "Alice", "age": 25},  # Valid
        {"name": "Bob", "age": "invalid"},  # Invalid age
    ]


@pytest.fixture
def rows_with_whitespace() -> list[dict[str, object]]:
    """Create rows with whitespace in keys and values."""
    return [
        {" name ": "Alice", "  age": 25},  # Valid
        {"name  ": "Bob", "age ": 30},  # Valid
        {"": "Charlie", "age": 35},  # Empty key after strip
    ]


@pytest.fixture
def validation_rules_rows() -> list[dict[str, object]]:
    """Create rows for ValidationRulesModel testing."""
    return [
        {"email": "valid@example.com", "score": 85, "status": "active"},  # Valid
        {"email": "invalid-email", "score": 85, "status": "active"},  # Invalid email
        {"email": "test@example.com", "score": 150, "status": "active"},  # Invalid score
        {"email": "test@example.com", "score": 85, "status": "x"},  # Invalid status length
    ]


@pytest.fixture
def aliased_fields_rows() -> list[dict[str, object]]:
    """Create rows with aliased field names."""
    return [
        {"userName": "alice", "userEmail": "alice@example.com"},
        {"user_name": "bob", "user_email": "bob@example.com"},  # Using original field names
    ]


@pytest.fixture
def example_model_rows() -> list[dict[str, object]]:
    """Create rows for ExampleModel testing."""
    return [
        {"author": "John Doe", "description": "Test", "code": "1234"},  # Valid
        {
            "author": "Jane Smith",
            "description": None,
            "code": "5678",
        },  # Valid with None description
        {"author": "Bob", "description": "Another test", "code": "ABC1"},  # Invalid code pattern
        {"author": "", "description": "Test", "code": "1234"},  # Invalid empty author
        {"description": "Test", "code": "1234"},  # Missing author
    ]


def test_valid_rows_success(valid_simple_rows: list[dict[str, object]]):
    """Test that valid rows are successfully validated and converted."""
    # GIVEN
    validator = ExcelValidationUseCase[SimpleTestModel](model=SimpleTestModel)

    # WHEN
    result = validator(valid_simple_rows)

    # THEN
    assert len(result) == 3
    assert all(isinstance(item, SimpleTestModel) for item in result)
    assert result[0].name == "Alice"
    assert result[0].age == 25
    assert result[1].name == "Bob"
    assert result[1].age == 30
    assert result[2].name == "Charlie"
    assert result[2].age == 35


def test_invalid_rows_raises_validation_error(invalid_simple_rows: list[dict[str, object]]):
    """Test that invalid rows raise RowValidationError."""
    # GIVEN
    validator = ExcelValidationUseCase[SimpleTestModel](model=SimpleTestModel)

    # WHEN & THEN
    with pytest.raises(RowValidationError) as exc_info:
        validator(invalid_simple_rows)

    errors = exc_info.value.errors
    assert len(errors) == 2

    # Check that errors have correct structure
    for error in errors:
        assert hasattr(error, "row_index")
        assert hasattr(error, "field")
        assert hasattr(error, "code")
        assert hasattr(error, "message")


def test_mixed_rows_partial_success(mixed_simple_rows: list[dict[str, object]]):
    """Test that mixed valid/invalid rows raise error but collect all errors."""
    # GIVEN
    validator = ExcelValidationUseCase[SimpleTestModel](model=SimpleTestModel)

    # WHEN & THEN
    with pytest.raises(RowValidationError) as exc_info:
        validator(mixed_simple_rows)

    errors = exc_info.value.errors
    assert len(errors) == 1

    # Verify row indices are correct (starting from 2 by default)
    error_row_indices = [error.row_index for error in errors]
    assert 3 in error_row_indices  # Row 4 with invalid age (0-based index)


def test_empty_rows_list():
    """Test validation with empty rows list."""
    # GIVEN
    validator = ExcelValidationUseCase[SimpleTestModel](model=SimpleTestModel)

    # WHEN
    result = validator([])

    # THEN
    assert result == []


def test_whitespace_handling(rows_with_whitespace: list[dict[str, object]]):
    """Test that whitespace in keys is properly stripped."""
    # GIVEN
    validator = ExcelValidationUseCase[SimpleTestModel](model=SimpleTestModel)

    # WHEN & THEN
    with pytest.raises(RowValidationError) as exc_info:
        validator(rows_with_whitespace)

    errors = exc_info.value.errors
    assert len(errors) == 1

    error_row_indices = [error.row_index for error in errors]
    assert 4 in error_row_indices  # Row with missing required field name


@pytest.mark.parametrize(
    "start_row_index,expected_first_error_row",
    [
        (1, 1),  # Excel row 1 (header row 0)
        (2, 2),  # Excel row 2 (default, header row 1)
        (5, 5),  # Excel row 5 (header row 4)
        (10, 10),  # Excel row 10 (header row 9)
    ],
)
def test_custom_start_row_index(start_row_index: int, expected_first_error_row: int):
    """Test that start_row_index affects error row numbering."""
    # GIVEN
    invalid_rows = [{"name": "Alice", "age": "invalid"}]
    validator = ExcelValidationUseCase[SimpleTestModel](
        model=SimpleTestModel, start_row_index=start_row_index
    )

    # WHEN & THEN
    with pytest.raises(RowValidationError) as exc_info:
        validator(invalid_rows)

    errors = exc_info.value.errors
    assert len(errors) >= 1
    assert errors[0].row_index == expected_first_error_row


def test_custom_error_mapper():
    """Test using a custom error mapper."""
    # GIVEN
    invalid_rows = [{"author": "John", "description": "Test", "code": "INVALID"}]
    custom_mapper = ExampleModelErrorMapper()
    validator = ExcelValidationUseCase[ExampleModel](model=ExampleModel, error_mapper=custom_mapper)

    # WHEN & THEN
    with pytest.raises(RowValidationError) as exc_info:
        validator(invalid_rows)

    errors = exc_info.value.errors
    assert len(errors) >= 1

    # Should use custom error messages from ExampleModelErrorMapper
    code_error = next((err for err in errors if err.field == "code"), None)
    assert code_error is not None
    assert "must be exactly 4 digits" in code_error.message


def test_default_error_mapper():
    """Test using the default error mapper."""
    # GIVEN
    invalid_rows = [{"name": "Alice", "age": "not_a_number"}]
    validator = ExcelValidationUseCase[SimpleTestModel](model=SimpleTestModel)

    # WHEN & THEN
    with pytest.raises(RowValidationError) as exc_info:
        validator(invalid_rows)

    errors = exc_info.value.errors
    assert len(errors) >= 1

    # Should use default error messages
    age_error = next((err for err in errors if err.field == "age"), None)
    assert age_error is not None
    assert "not_a_number" in age_error.message  # Should include input value


def test_validation_rules_model(validation_rules_rows: list[dict[str, object]]):
    """Test validation with complex validation rules."""
    # GIVEN
    validator = ExcelValidationUseCase[ValidationRulesModel](model=ValidationRulesModel)

    # WHEN & THEN
    with pytest.raises(RowValidationError) as exc_info:
        validator(validation_rules_rows)

    errors = exc_info.value.errors
    assert len(errors) == 3

    error_codes = [error.code for error in errors]
    assert "string_pattern_mismatch" in error_codes  # Email pattern
    assert "less_than_equal" in error_codes  # Score range
    assert "string_too_short" in error_codes  # Status length


def test_optional_fields_validation():
    """Test validation with optional fields."""
    # GIVEN
    rows = [
        {"required_field": "test"},  # Missing optional field - should be OK
        {"required_field": "test", "optional_field": "value"},  # Both fields - should be OK
        {"optional_field": "value"},  # Missing required field - should fail
    ]
    validator = ExcelValidationUseCase[OptionalFieldsModel](model=OptionalFieldsModel)

    # WHEN & THEN
    with pytest.raises(RowValidationError) as exc_info:
        validator(cast(list[dict[str, object]], rows))

    errors = exc_info.value.errors
    assert len(errors) == 1
    assert errors[0].field == "requiredField"
    assert errors[0].row_index == 4  # Third row


def test_aliased_fields_handling(aliased_fields_rows: list[dict[str, object]]):
    """Test handling of aliased field names."""
    # GIVEN
    validator = ExcelValidationUseCase[AliasedFieldsModel](model=AliasedFieldsModel)

    # WHEN
    result = validator(aliased_fields_rows)

    # THEN
    assert len(result) == 2
    assert result[0].user_name == "alice"
    assert result[0].user_email == "alice@example.com"
    assert result[1].user_name == "bob"
    assert result[1].user_email == "bob@example.com"


def test_display_field_name_method():
    """Test the _display_field_name method with aliases."""
    # GIVEN
    validator = ExcelValidationUseCase[AliasedFieldsModel](model=AliasedFieldsModel)

    # WHEN & THEN
    assert validator._display_field_name("user_name") == "userName"  # Should return alias
    assert validator._display_field_name("user_email") == "userEmail"  # Should return alias
    assert (
        validator._display_field_name("nonexistent_field") == "nonexistent_field"
    )  # Should return original
    assert validator._display_field_name(None) is None  # Should handle None


@pytest.mark.parametrize(
    "invalid_row,expected_error_field,expected_error_code",
    [
        ({"name": "Alice", "age": "text"}, "age", "int_parsing"),
        ({"age": 25}, "name", "missing"),
        ({"name": 123, "age": 25}, "name", "string_type"),
    ],
)
def test_specific_validation_errors(
    invalid_row: dict[str, object], expected_error_field: str, expected_error_code: str
):
    """Test specific validation error scenarios."""
    # GIVEN
    validator = ExcelValidationUseCase[SimpleTestModel](model=SimpleTestModel)

    # WHEN & THEN
    with pytest.raises(RowValidationError) as exc_info:
        validator([invalid_row])

    errors = exc_info.value.errors
    field_error = next((err for err in errors if err.field == expected_error_field), None)
    assert field_error is not None
    assert field_error.code == expected_error_code


def test_multiple_errors_same_row():
    """Test that multiple validation errors in the same row are collected."""
    # GIVEN
    invalid_row = [{"name": 1337, "age": "not_a_number"}]  # Two errors in one row
    validator = ExcelValidationUseCase[SimpleTestModel](model=SimpleTestModel)

    # WHEN & THEN
    with pytest.raises(RowValidationError) as exc_info:
        validator(invalid_row)

    errors = exc_info.value.errors
    assert len(errors) == 2

    # Both errors should be for the same row
    row_indices = [error.row_index for error in errors]
    assert all(row_index == 2 for row_index in row_indices)  # All errors for first data row


def test_context_information_in_errors():
    """Test that error context information is properly passed through."""
    # GIVEN
    invalid_rows = [{"email": "invalid", "score": 150, "status": "x"}]
    validator = ExcelValidationUseCase[ValidationRulesModel](model=ValidationRulesModel)

    # WHEN & THEN
    with pytest.raises(RowValidationError) as exc_info:
        validator(invalid_rows)

    errors = exc_info.value.errors

    # Check that input values are included in error messages
    for error in errors:
        assert error.message is not None
        assert len(error.message) > 0
        # Error messages should contain the invalid input value
        if error.field == "email":
            assert "invalid" in error.message
        elif error.field == "score":
            assert "150" in error.message
        elif error.field == "status":
            assert "x" in error.message


def test_successful_validation_returns_correct_types():
    """Test that successful validation returns correctly typed domain models."""
    # GIVEN
    valid_rows = [{"name": "Alice", "age": 25}]
    validator = ExcelValidationUseCase[SimpleTestModel](model=SimpleTestModel)

    # WHEN
    result = validator(valid_rows)

    # THEN
    assert len(result) == 1
    item = result[0]
    assert isinstance(item, SimpleTestModel)
    assert isinstance(item.name, str)
    assert isinstance(item.age, int)
    assert item.name == "Alice"
    assert item.age == 25
