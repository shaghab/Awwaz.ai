"""Canonical errors and global handlers (PRD §19)."""

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from app.core.envelope import err

logger = logging.getLogger("awwaz")


class AppError(Exception):
    code = "INTERNAL_ERROR"
    http_status = 500
    default_message = "Something went wrong. Please try again."

    def __init__(
        self, message: str | None = None, *, details: Any = None, code: str | None = None
    ) -> None:
        self.message = message or self.default_message
        self.details = details
        if code:
            self.code = code
        super().__init__(self.message)


class ValidationError(AppError):
    code = "VALIDATION_ERROR"
    http_status = 400
    default_message = "Invalid request."


class Unauthorized(AppError):
    code = "UNAUTHORIZED"
    http_status = 401
    default_message = "Sign in to continue."


class Forbidden(AppError):
    code = "FORBIDDEN"
    http_status = 403
    default_message = "You do not have permission to do that."


class NotFound(AppError):
    code = "NOT_FOUND"
    http_status = 404
    default_message = "Not found."


class Conflict(AppError):
    code = "CONFLICT"
    http_status = 409
    default_message = "The resource changed. Refresh to see the latest state."


class InvalidStateTransition(AppError):
    code = "INVALID_STATE_TRANSITION"
    http_status = 409
    default_message = "That status change is not allowed."


class RateLimited(AppError):
    code = "RATE_LIMITED"
    http_status = 429
    default_message = "Too many requests. Please wait and try again."


class AIUnavailable(AppError):
    code = "AI_UNAVAILABLE"
    http_status = 503
    default_message = "The assistant is unavailable right now. Nothing was created."


class AIInvalidOutput(AppError):
    code = "AI_INVALID_OUTPUT"
    http_status = 502
    default_message = "I couldn't confidently process that request. No complaint was created."


class ExternalServiceUnavailable(AppError):
    code = "EXTERNAL_SERVICE_UNAVAILABLE"
    http_status = 503
    default_message = "A required service is unavailable. No action was confirmed."


class ActionAlreadyExecuted(AppError):
    code = "ACTION_ALREADY_EXECUTED"
    http_status = 409
    default_message = "That action was already executed."


class StorageFailure(AppError):
    code = "STORAGE_FAILURE"
    http_status = 503
    default_message = "The file could not be stored. Nothing was saved."


class InternalError(AppError):
    pass


class UnhandledErrorMiddleware(BaseHTTPMiddleware):
    """Turn an unhandled exception into the canonical envelope from *inside* the
    user middleware stack.

    Starlette's ServerErrorMiddleware wraps everything added with
    `add_middleware`, so a 500 it builds never travels back out through CORS,
    access logging, or request-ID tagging: cross-origin the browser cannot even
    read the body, and the response carries no X-Request-ID. Catching here makes
    the error an ordinary response on the way out, so it picks all three up.

    Mounted innermost (added first in the app factory). The registered
    `Exception` handler stays as a last resort for anything raised in the
    middleware layered outside this one.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            return await call_next(request)
        except Exception:
            # Stack trace stays server-side (PRD §19, §23).
            logger.exception("unhandled_exception")
            return JSONResponse(
                status_code=500,
                content=err("INTERNAL_ERROR", InternalError.default_message),
            )


_HTTP_STATUS_TO_CODE = {
    400: "VALIDATION_ERROR",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "NOT_FOUND",
    409: "CONFLICT",
    429: "RATE_LIMITED",
    503: "EXTERNAL_SERVICE_UNAVAILABLE",
}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.http_status,
            content=err(exc.code, exc.message, details=exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content=err("VALIDATION_ERROR", ValidationError.default_message),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = _HTTP_STATUS_TO_CODE.get(exc.status_code, "INTERNAL_ERROR")
        message = exc.detail if isinstance(exc.detail, str) else "Request failed."
        return JSONResponse(status_code=exc.status_code, content=err(code, message))

    @app.exception_handler(Exception)
    async def _unhandled(_: Request, exc: Exception) -> JSONResponse:
        # Stack trace stays server-side (PRD §19, §23).
        logger.exception("unhandled_exception")
        return JSONResponse(
            status_code=500, content=err("INTERNAL_ERROR", InternalError.default_message)
        )
