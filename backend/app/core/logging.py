"""Structured JSON logging (PRD §23). Never logs cookies, secrets, or message bodies."""

import json
import logging
import sys
import time
from collections.abc import Awaitable, Callable
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.request_id import get_request_id


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None) or get_request_id(),
        }
        for key in ("route", "status", "duration_ms", "method"):
            value = getattr(record, key, None)
            if value is not None:
                payload[key] = value
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
    for noisy in ("uvicorn.access",):
        logging.getLogger(noisy).handlers = []
        logging.getLogger(noisy).propagate = False


class AccessLogMiddleware(BaseHTTPMiddleware):
    """One structured line per request. Query strings and bodies are never logged."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        started = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            logging.getLogger("awwaz.access").exception(
                "request_failed",
                extra={
                    "route": request.url.path,
                    "method": request.method,
                    "status": 500,
                    "duration_ms": round((time.perf_counter() - started) * 1000, 2),
                },
            )
            raise
        logging.getLogger("awwaz.access").info(
            "request",
            extra={
                "route": request.url.path,
                "method": request.method,
                "status": response.status_code,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
            },
        )
        return response
