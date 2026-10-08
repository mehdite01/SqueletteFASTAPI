import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.application.exceptions import ApplicationError
from app.presentation.responses import (
    ApiError,
    ApiErrorResponse,
)

logger = logging.getLogger("app.errors")


def get_request_id(request: Request) -> str | None:
    return request.headers.get("X-Request-ID")


def create_error_response(
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: object | None = None,
) -> JSONResponse:
    response = ApiErrorResponse(
        error=ApiError(
            code=code,
            message=message,
            details=details,
        )
    )

    request_id = get_request_id(request)

    headers: dict[str, str] = {}

    if request_id is not None:
        headers["X-Request-ID"] = request_id

    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(),
        headers=headers,
    )


async def application_error_handler(
    request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    return create_error_response(
        request=request,
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    return create_error_response(
        request=request,
        status_code=exc.status_code,
        code="HTTP_ERROR",
        message=str(exc.detail),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return create_error_response(
        request=request,
        status_code=422,
        code="VALIDATION_ERROR",
        message="Request validation failed.",
        details=exc.errors(),
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "Unhandled exception on %s %s",
        request.method,
        request.url.path,
    )

    return create_error_response(
        request=request,
        status_code=500,
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
    )