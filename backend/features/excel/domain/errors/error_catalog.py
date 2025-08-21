from typing import Any

DEFAULT_ERROR_CATALOG: dict[str, Any] = {
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
    "fields": {
        # per-field overrides (match by model field name or alias; see mapper helper below)
        "email": {
            "string_pattern_mismatch": "Please enter a valid email like name@example.com.",
        },
        "Birth Date": {  # example using alias as the match key
            "date_parsing": "Birth Date must be YYYY-MM-DD (e.g., 1990-04-23).",
        },
    },
}
