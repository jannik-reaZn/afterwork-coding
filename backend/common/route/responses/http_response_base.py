from http import HTTPStatus
from typing import Any, Optional, Type

from pydantic import BaseModel, ConfigDict, Field


class HttpResponseBase(BaseModel):
    title: str
    description: str
    code: HTTPStatus = Field(description="All HTTPStatus Codes")

    model_config = ConfigDict(
        use_enum_values=True,
    )

    @staticmethod
    def to_default_example(
        httpStatus: HTTPStatus,
        model: Type[BaseModel],
        description: Optional[str] = None,
        example: Optional[Any] = None,
    ):
        return {
            "model": model,
            "description": (description if description is not None else httpStatus.phrase),
            "content": {
                "application/json": {
                    "example": (
                        example
                        if example is not None
                        else {
                            "title": httpStatus.phrase,
                            "description": (
                                description if description is not None else httpStatus.description
                            ),
                            "code": httpStatus.value,
                        }
                    ),
                }
            },
        }
