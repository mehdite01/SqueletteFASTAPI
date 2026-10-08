from uuid import uuid4

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.request_context import set_request_id

REQUEST_ID_HEADER = "X-Request-ID"


class RequestIdMiddleware:
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

        request_id = self._get_request_id(
            scope,
        )

        set_request_id(request_id)

        async def send_with_request_id(
            message: Message,
        ) -> None:
            if message["type"] == "http.response.start":
                headers = list(
                    message.get("headers", [])
                )

                headers.append(
                    (
                        REQUEST_ID_HEADER.lower().encode(),
                        request_id.encode(),
                    )
                )

                message["headers"] = headers

            await send(message)

        await self.app(
            scope,
            receive,
            send_with_request_id,
        )

    @staticmethod
    def _get_request_id(
        scope: Scope,
    ) -> str:
        for key, value in scope.get(
            "headers",
            [],
        ):
            if (
                key.lower()
                == REQUEST_ID_HEADER.lower().encode()
            ):
                decoded = value.decode(
                    "utf-8"
                ).strip()

                if decoded:
                    return decoded

        return str(uuid4())