from http import HTTPStatus
from typing import Any, Optional

from .http_response_base import HttpResponseBase


class Created(HttpResponseBase):
    @staticmethod
    def to_example(
        model: Any = None,
        description: Optional[str] = None,
        example: Optional[Any] = None,
    ):
        return HttpResponseBase.to_default_example(
            httpStatus=HTTPStatus.CREATED,
            model=(model if model is not None else Created),
            description=description,
            example=example,
        )
