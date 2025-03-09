from http import HTTPStatus
from typing import Any, Optional

from .http_response_base import HttpResponseBase


class UnprocessableEntity(HttpResponseBase):
    @staticmethod
    def to_example(description: Optional[str] = None, example: Optional[Any] = None):
        return HttpResponseBase.to_default_example(
            httpStatus=HTTPStatus.UNPROCESSABLE_ENTITY,
            model=UnprocessableEntity,
            description=description,
            example=example,
        )
