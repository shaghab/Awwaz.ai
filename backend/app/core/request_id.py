"""Request ID propagation (PRD §23)."""

import uuid
from collections.abc import Awaitable, Callable
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

HEADER = "X-Request-ID"
_request_id: ContextVar[str] = ContextVar("request_id", default="req_unset")


def new_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:26]}"


def get_request_id() -> str:
    return _request_id.get()


def set_request_id(value: str) -> None:
    _request_id.set(value)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Echo an incoming request ID or mint one, and expose it on the response."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        incoming = request.headers.get(HEADER)
        request_id = incoming if incoming and len(incoming) <= 128 else new_request_id()
        set_request_id(request_id)
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[HEADER] = request_id
        return response
