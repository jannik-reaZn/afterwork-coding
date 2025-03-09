from http import HTTPStatus
from typing import Any, Optional

from backend.common.route.responses import HttpResponseBase


class OK(HttpResponseBase):
    @staticmethod
    def to_example(
        model: Any = None,
        description: Optional[str] = None,
        example: Optional[Any] = None,
    ):
        return HttpResponseBase.to_default_example(
            httpStatus=HTTPStatus.OK,
            model=(model if model is not None else OK),
            description=description,
            example=example,
        )
