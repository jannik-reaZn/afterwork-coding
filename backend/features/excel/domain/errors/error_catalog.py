from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

# Shape:
#  codes: {"pydantic_code": "Message with {placeholders}"}
#  fields: {"field_or_alias": {"pydantic_code": "Message"}}
#  default: "Fallback message"
CatalogDict = Mapping[str, Any]


@dataclass(frozen=True)
class ErrorCatalog:
    codes: Mapping[str, str]
    fields: Mapping[str, Mapping[str, str]]
    default: str

    @staticmethod
    def from_dict(d: CatalogDict) -> ErrorCatalog:
        return ErrorCatalog(
            codes=d.get("codes", {}) or {},
            fields=d.get("fields", {}) or {},
            default=d.get("default", "Invalid value."),
        )

    def resolve(self, *, field: Optional[str], code: str) -> Optional[str]:
        if field and field in self.fields and code in self.fields[field]:
            return self.fields[field][code]
        if code in self.codes:
            return self.codes[code]
        return None

    @staticmethod
    def merge(*catalogs: ErrorCatalog) -> ErrorCatalog:
        """
        Later catalogs override earlier ones (right-most wins).
        """
        codes: Dict[str, str] = {}
        fields: Dict[str, Dict[str, str]] = {}
        default = "Invalid value."

        for c in catalogs:
            codes.update(c.codes)
            # deep merge for fields
            for f, mapping in c.fields.items():
                fields.setdefault(f, {}).update(mapping)
            default = c.default or default

        return ErrorCatalog(codes=codes, fields=fields, default=default)
