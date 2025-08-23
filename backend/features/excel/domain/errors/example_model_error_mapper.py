from typing import Any

from backend.features.excel.domain.errors.default_error_catalog import DEFAULT_ERROR_CATALOG
from backend.features.excel.domain.errors.error_catalog import ErrorCatalog
from backend.features.excel.domain.errors.error_mapper import ErrorMapper


class ExampleModelErrorMapper(ErrorMapper):
    """
    Custom error mapper for ExampleModel with field-specific error messages.
    Combines the default catalog with model-specific field overrides.
    """

    def __init__(self):
        # Create field-specific error messages for ExampleModel
        example_model_overrides = ErrorCatalog.from_dict(
            {
                "codes": {},  # Inherit all default codes
                "default": "",  # Inherit default message
                "fields": {
                    "code": {
                        "string_pattern_mismatch": (
                            "Code '{input_value}' must be exactly 4 digits (e.g., 1234)."
                        ),
                        "string_type": (
                            "Code '{input_value}' must be a text value containing 4 digits."
                        ),
                    },
                    "author": {
                        "missing": "Author name is required.",
                        "string_type": "Author '{input_value}' must be a text value.",
                    },
                    "description": {
                        "string_type": "Description '{input_value}' must be a text value.",
                    },
                },
            }
        )

        # Merge default catalog with field-specific overrides
        combined_catalog = ErrorCatalog.merge(DEFAULT_ERROR_CATALOG, example_model_overrides)
        super().__init__(combined_catalog)
