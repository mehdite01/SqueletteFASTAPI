from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.application.exceptions import ApplicationError
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.middleware.request_id import RequestIdMiddleware
from app.core.middleware.request_logging import (
    RequestLoggingMiddleware,
)
from app.core.middleware.request_timing import (
    RequestTimingMiddleware,
)
from app.presentation.exception_handlers import (
    application_error_handler,
    http_exception_handler,
    unexpected_exception_handler,
    validation_exception_handler,
)
from app.presentation.test_entities_router import (
    router as test_entities_router,
)


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        RequestIdMiddleware,
    )

    app.add_middleware(
        RequestTimingMiddleware,
    )

    app.add_middleware(
        RequestLoggingMiddleware,
    )

    app.add_exception_handler(
        ApplicationError,
        application_error_handler,
    )

    app.add_exception_handler(
        StarletteHTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unexpected_exception_handler,
    )

    app.include_router(
        test_entities_router,
    )

    @app.get(
        "/health",
        tags=["Health"],
    )
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
        }

    return app


app = create_app()