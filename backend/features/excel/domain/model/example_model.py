from pydantic import Field

from backend.common.domain.models.domain_model import DomainModel


class ExampleModel(DomainModel):
    author: str = Field()
    description: str | None = Field(default=None)
    code: str = Field(pattern=r"^\d{4}$")
