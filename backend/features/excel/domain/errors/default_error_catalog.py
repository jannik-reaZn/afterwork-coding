from backend.features.excel.domain.errors.error_catalog import ErrorCatalog

DEFAULT_ERROR_CATALOG = ErrorCatalog.from_dict(
    {
        "codes": {
            "string_pattern_mismatch": "Invalid format for '{input_value}'. Expected format not met.",  # noqa: E501
            "bool_parsing": "'{input_value}' is not a valid boolean. Must be true/false.",
            "int_parsing": "'{input_value}' is not a valid integer. Must be a whole number.",
            "float_parsing": "'{input_value}' is not a valid number.",
            "date_parsing": "'{input_value}' is not a valid date. Use format YYYY-MM-DD.",
            "missing": "This field is required.",
            "too_short": "'{input_value}' is too short (min {min_length} characters).",
            "too_long": "'{input_value}' is too long (max {max_length} characters).",
            "greater_than": "'{input_value}' must be greater than {gt}.",
            "greater_than_equal": "'{input_value}' must be at least {ge}.",
            "less_than": "'{input_value}' must be less than {lt}.",
            "less_than_equal": "'{input_value}' must be at most {le}.",
            "not_in_enum": "'{input_value}' is not a supported value.",
            "string_type": "'{input_value}' is not a valid text value.",
            "value_error": "'{input_value}' is not a valid value.",
        },
        "default": "Invalid value '{input_value}'.",
        "fields": {},
    }
)
