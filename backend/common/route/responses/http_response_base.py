from http import HTTPStatus
from typing import Any, Optional, Type

from pydantic import BaseModel, Field


class HttpResponseBase(BaseModel):
    title: str
    description: str
    code: HTTPStatus = Field(description="All HTTPStatus Codes")

    @staticmethod
    def to_default_example(
        httpsStatus: HTTPStatus,
        model: Type[BaseModel],
        description: Optional[str] = None,
        example: Optional[Any] = None,
    ):
        pass
