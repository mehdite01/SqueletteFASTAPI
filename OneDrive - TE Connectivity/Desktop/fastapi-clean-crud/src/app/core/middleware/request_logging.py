import logging
import time

from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.request_context import get_request_id


logger = logging.getLogger("app.request")


class RequestLoggingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(
                scope,
                receive,
                send,
            )
            return

        method = scope.get(
            "method",
            "",
        )

        path = scope.get(
            "path",
            "",
        )

        status_code = 500
        start = time.perf_counter()

        async def send_with_logging(
            message,
        ):
            nonlocal status_code

            if message["type"] == "http.response.start":
                status_code = message["status"]

            await send(message)

        try:
            await self.app(
                scope,
                receive,
                send_with_logging,
            )
        finally:
            elapsed = (
                time.perf_counter() - start
            ) * 1000

            logger.info(
                "%s %s -> %s (%.2f ms)",
                method,
                path,
                status_code,
                elapsed,
                extra={
                    "request_id": get_request_id(),
                },
            )