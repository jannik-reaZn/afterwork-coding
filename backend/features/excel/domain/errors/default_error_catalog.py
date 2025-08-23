from backend.features.excel.domain.errors.error_catalog import ErrorCatalog

DEFAULT_ERROR_CATALOG = ErrorCatalog.from_dict(
    {
        "codes": {
            "string_pattern_mismatch": "Invalid format.",
            "bool_parsing": "Must be true/false.",
            "int_parsing": "Must be an integer.",
            "float_parsing": "Must be a number.",
            "date_parsing": "Use date format YYYY-MM-DD.",
            "missing": "This field is required.",
            "too_short": "Too short (min {min_length}).",
            "too_long": "Too long (max {max_length}).",
            "greater_than": "Must be greater than {gt}.",
            "greater_than_equal": "Must be at least {ge}.",
            "less_than": "Must be less than {lt}.",
            "less_than_equal": "Must be at most {le}.",
            "not_in_enum": "Unsupported value.",
        },
        "default": "Invalid value.",
        "fields": {},
    }
)
