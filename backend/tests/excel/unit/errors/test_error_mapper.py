from typing import Any

import pytest

from backend.features.excel.domain.errors.error_catalog import ErrorCatalog
from backend.features.excel.domain.errors.error_mapper import ErrorMapper
from backend.features.excel.domain.errors.user_friendly_error import UserFriendlyError


@pytest.fixture
def basic_error_catalog() -> ErrorCatalog:
    """Create a basic error catalog for testing."""
    return ErrorCatalog.from_dict(
        {
            "codes": {
                "string_pattern_mismatch": (
                    "Invalid format for '{input_value}'. Expected pattern not met."
                ),
                "missing": "This field is required.",
                "int_parsing": "'{input_value}' is not a valid integer.",
                "string_type": "'{input_value}' must be a text value.",
                "too_short": "'{input_value}' is too short (minimum {min_length} characters).",
                "greater_than": "'{input_value}' must be greater than {gt}.",
            },
            "fields": {
                "code": {
                    "string_pattern_mismatch": (
                        "Code '{input_value}' must be exactly 4 digits (e.g., 1234)."
                    ),
                    "string_type": "Code '{input_value}' must be a text value containing digits.",
                },
                "email": {
                    "string_pattern_mismatch": "'{input_value}' is not a valid email address.",
                },
                "age": {
                    "int_parsing": "Age '{input_value}' must be a valid number.",
                    "greater_than": "Age '{input_value}' must be greater than {gt}.",
                },
            },
            "default": "Invalid value '{input_value}'.",
        }
    )


@pytest.fixture
def empty_error_catalog() -> ErrorCatalog:
    """Create an empty error catalog for testing fallback behavior."""
    return ErrorCatalog.from_dict(
        {
            "codes": {},
            "fields": {},
            "default": "Something went wrong.",
        }
    )


@pytest.fixture
def catalog_with_malformed_templates() -> ErrorCatalog:
    """Create an error catalog with malformed message templates for testing exception handling."""
    return ErrorCatalog.from_dict(
        {
            "codes": {
                "malformed_template": "Invalid {missing_closing_brace",
                "missing_placeholder": "Value {nonexistent_var} is invalid.",
                "complex_malformed": "Error {unclosed and {nested} template",
            },
            "fields": {
                "test_field": {
                    "bad_format": "Field {bad_placeholder with spaces} is wrong.",
                }
            },
            "default": "Default message with {missing_var}.",
        }
    )


@pytest.fixture
def basic_error_mapper(basic_error_catalog: ErrorCatalog) -> ErrorMapper:
    """Create an ErrorMapper with basic catalog."""
    return ErrorMapper(basic_error_catalog)


@pytest.fixture
def empty_error_mapper(empty_error_catalog: ErrorCatalog) -> ErrorMapper:
    """Create an ErrorMapper with empty catalog."""
    return ErrorMapper(empty_error_catalog)


@pytest.fixture
def malformed_error_mapper(catalog_with_malformed_templates: ErrorCatalog) -> ErrorMapper:
    """Create an ErrorMapper with malformed templates for exception testing."""
    return ErrorMapper(catalog_with_malformed_templates)


def test_map_with_field_specific_message(basic_error_mapper: ErrorMapper):
    """Test mapping with field-specific error message."""
    # GIVEN
    row_index = 5
    field = "code"
    code = "string_pattern_mismatch"
    input_value = "ABC123"

    # WHEN
    result = basic_error_mapper.map(
        row_index=row_index, field=field, code=code, input_value=input_value
    )

    # THEN
    assert isinstance(result, UserFriendlyError)
    assert result.row_index == row_index
    assert result.field == field
    assert result.code == code
    assert result.message == "Code 'ABC123' must be exactly 4 digits (e.g., 1234)."


def test_map_with_global_code_message(basic_error_mapper: ErrorMapper):
    """Test mapping with global code message when no field-specific message exists."""
    # GIVEN
    row_index = 3
    field = "username"  # Field not in catalog
    code = "string_pattern_mismatch"
    input_value = "invalid@user"

    # WHEN
    result = basic_error_mapper.map(
        row_index=row_index, field=field, code=code, input_value=input_value
    )

    # THEN
    assert result.row_index == row_index
    assert result.field == field
    assert result.code == code
    assert result.message == "Invalid format for 'invalid@user'. Expected pattern not met."


def test_map_with_default_message(basic_error_mapper: ErrorMapper):
    """Test mapping falls back to default message when code not found."""
    # GIVEN
    row_index = 2
    field = "unknown_field"
    code = "unknown_code"
    input_value = "test_value"

    # WHEN
    result = basic_error_mapper.map(
        row_index=row_index, field=field, code=code, input_value=input_value
    )

    # THEN
    assert result.row_index == row_index
    assert result.field == field
    assert result.code == code
    assert result.message == "Invalid value 'test_value'."


def test_map_with_context_variables(basic_error_mapper: ErrorMapper):
    """Test mapping with additional context variables."""
    # GIVEN
    row_index = 4
    field = "password"
    code = "too_short"
    input_value = "123"
    ctx = {"min_length": 8}

    # WHEN
    result = basic_error_mapper.map(
        row_index=row_index, field=field, code=code, input_value=input_value, ctx=ctx
    )

    # THEN
    assert result.message == "'123' is too short (minimum 8 characters)."


def test_map_with_none_field(basic_error_mapper: ErrorMapper):
    """Test mapping with None field value."""
    # GIVEN
    row_index = 1
    field = None
    code = "missing"

    # WHEN
    result = basic_error_mapper.map(row_index=row_index, field=field, code=code)

    # THEN
    assert result.row_index == row_index
    assert result.field is None
    assert result.code == code
    assert result.message == "This field is required."


def test_map_with_default_raw_message_fallback():
    """Test mapping falls back to default_raw_msg when catalog has no matches and no default."""
    # GIVEN
    # Create a catalog with truly empty default to test default_raw_msg fallback
    truly_empty_catalog = ErrorCatalog.from_dict(
        {
            "codes": {},
            "fields": {},
            "default": "",  # Empty default so default_raw_msg can be used
        }
    )
    mapper = ErrorMapper(truly_empty_catalog)

    row_index = 7
    field = "test_field"
    code = "unknown_error"
    default_raw_msg = "Raw validation error message"

    # WHEN
    result = mapper.map(
        row_index=row_index, field=field, code=code, default_raw_msg=default_raw_msg
    )

    # THEN
    assert result.message == default_raw_msg


def test_map_with_ultimate_fallback(empty_error_mapper: ErrorMapper):
    """Test mapping with ultimate fallback when all other options are None."""
    # Create a catalog with no default
    catalog = ErrorCatalog.from_dict(
        {
            "codes": {},
            "fields": {},
            "default": "",  # Empty default
        }
    )
    mapper = ErrorMapper(catalog)

    # GIVEN
    row_index = 8
    field = "test"
    code = "unknown"

    # WHEN
    result = mapper.map(row_index=row_index, field=field, code=code)

    # THEN
    assert result.message == "Invalid value."  # Ultimate fallback


@pytest.mark.parametrize(
    "row_index,field,code,input_value,expected_message_part",
    [
        (1, "email", "string_pattern_mismatch", "invalid-email", "not a valid email address"),
        (2, "age", "int_parsing", "not_a_number", "must be a valid number"),
        (3, "age", "greater_than", "5", "must be greater than"),
        (4, "code", "string_type", 12345, "must be a text value containing digits"),
        (5, None, "missing", None, "This field is required"),
    ],
)
def test_map_various_scenarios(
    basic_error_mapper: ErrorMapper,
    row_index: int,
    field: str | None,
    code: str,
    input_value: Any,
    expected_message_part: str,
):
    """Test various mapping scenarios with parameterized inputs."""
    # WHEN
    result = basic_error_mapper.map(
        row_index=row_index, field=field, code=code, input_value=input_value
    )

    # THEN
    assert result.row_index == row_index
    assert result.field == field
    assert result.code == code
    assert expected_message_part in result.message
    if input_value is not None:
        assert str(input_value) in result.message


def test_map_malformed_template_handling(malformed_error_mapper: ErrorMapper):
    """Test that malformed templates are handled gracefully."""
    # GIVEN
    row_index = 10
    field = "test_field"
    code = "bad_format"
    input_value = "test_value"

    # WHEN
    result = malformed_error_mapper.map(
        row_index=row_index, field=field, code=code, input_value=input_value
    )

    # THEN
    assert result.row_index == row_index
    assert result.field == field
    assert result.code == code
    # Should use the original template since formatting failed
    assert result.message == "Field {bad_placeholder with spaces} is wrong."


def test_map_missing_context_variable(basic_error_mapper: ErrorMapper):
    """Test handling when template requires context variable that's not provided."""
    # GIVEN
    row_index = 6
    field = "age"
    code = "greater_than"
    input_value = "5"
    # Not providing 'gt' context variable that the template expects

    # WHEN
    result = basic_error_mapper.map(
        row_index=row_index, field=field, code=code, input_value=input_value
    )

    # THEN
    assert result.row_index == row_index
    assert result.field == field
    assert result.code == code
    # Should use the original template since formatting failed
    assert result.message == "Age '5' must be greater than {gt}."


def test_map_complex_context_with_special_characters():
    """Test mapping with context containing special characters."""
    # GIVEN
    catalog = ErrorCatalog.from_dict(
        {
            "codes": {
                "custom_error": "Value '{input_value}' failed validation: {reason}",
            },
            "fields": {},
            "default": "Error occurred.",
        }
    )
    mapper = ErrorMapper(catalog)

    row_index = 9
    field = "description"
    code = "custom_error"
    input_value = "Test with 'quotes' and {braces}"
    ctx = {"reason": "Contains special characters: $@#%"}

    # WHEN
    result = mapper.map(
        row_index=row_index, field=field, code=code, input_value=input_value, ctx=ctx
    )

    # THEN
    expected_message = (
        "Value 'Test with 'quotes' and {braces}' failed validation: "
        "Contains special characters: $@#%"
    )
    assert result.message == expected_message


def test_map_input_value_none_handling(basic_error_mapper: ErrorMapper):
    """Test handling when input_value is None."""
    # GIVEN
    row_index = 11
    field = "required_field"
    code = "missing"
    input_value = None

    # WHEN
    result = basic_error_mapper.map(
        row_index=row_index, field=field, code=code, input_value=input_value
    )

    # THEN
    assert result.row_index == row_index
    assert result.field == field
    assert result.code == code
    assert result.message == "This field is required."
    # input_value should not be added to context when None


def test_map_empty_context_dict(basic_error_mapper: ErrorMapper):
    """Test mapping with explicitly empty context dict."""
    # GIVEN
    row_index = 12
    field = "test_field"
    code = "string_type"
    input_value = 42
    ctx = {}

    # WHEN
    result = basic_error_mapper.map(
        row_index=row_index, field=field, code=code, input_value=input_value, ctx=ctx
    )

    # THEN
    assert result.message == "'42' must be a text value."


def test_error_mapper_initialization():
    """Test ErrorMapper initialization with different catalogs."""
    # GIVEN
    catalog = ErrorCatalog.from_dict({"codes": {}, "fields": {}, "default": "Test default"})

    # WHEN
    mapper = ErrorMapper(catalog)

    # THEN
    assert mapper.catalog == catalog
    assert mapper.catalog.default == "Test default"


@pytest.mark.parametrize(
    "malformed_template,expected_behavior",
    [
        ("Missing {unclosed_brace", "uses original template"),
        ("Invalid {}", "uses original template"),
        ("{nonexistent_var} not found", "uses original template"),
        ("Multiple {missing} {vars}", "uses original template"),
    ],
)
def test_malformed_template_scenarios(malformed_template: str, expected_behavior: str):
    """Test various malformed template scenarios."""
    # GIVEN
    catalog = ErrorCatalog.from_dict(
        {
            "codes": {"test_code": malformed_template},
            "fields": {},
            "default": "Default message",
        }
    )
    mapper = ErrorMapper(catalog)

    # WHEN
    result = mapper.map(row_index=1, field="test_field", code="test_code", input_value="test_value")

    # THEN
    if expected_behavior == "uses original template":
        assert result.message == malformed_template
