from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.common.route.responses import HttpResponseBase
from backend.logger import logger


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Server Error: {exc} | URL: {request.url}", exc_info=True)
    response_model = HttpResponseBase(
        title="Internal Server Error",
        description="Something went wrong.",
        code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content=response_model.model_dump(),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    logger.error(f"HTTP Error {exc.status_code}: {exc.detail} | URL: {request.url}")
    response_model = HttpResponseBase(
        title=str(exc.__class__.__name__),
        description=str(exc.detail),
        code=HTTPStatus(exc.status_code),
    )

    return JSONResponse(status_code=exc.status_code, content=response_model.model_dump())


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    response_model = HttpResponseBase(
        title=str(exc.__class__.__name__),
        description="The server was unable to process the request, because it contains invalid data.",
        code=HTTPStatus(HTTPStatus.UNPROCESSABLE_ENTITY),
    )

    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY, content=response_model.model_dump()
    )


def register_exception_handlers(app: FastAPI) -> None:
    # exception handlers are registered and catch errors in bottom to top order

    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(ValidationError, request_validation_exception_handler)
