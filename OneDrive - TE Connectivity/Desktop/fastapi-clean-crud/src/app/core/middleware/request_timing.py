import time

from starlette.types import ASGIApp, Receive, Scope, Send


class RequestTimingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.perf_counter()

        async def send_with_timing(message):
            if message["type"] == "http.response.start":
                elapsed = time.perf_counter() - start

                headers = list(
                    message.get("headers", [])
                )

                headers.append(
                    (
                        b"x-process-time-ms",
                        f"{elapsed * 1000:.2f}".encode(),
                    )
                )

                message["headers"] = headers

            await send(message)

        await self.app(
            scope,
            receive,
            send_with_timing,
        )