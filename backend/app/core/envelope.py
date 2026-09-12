"""Response envelope (PRD §12)."""

from typing import Any

from app.core.request_id import get_request_id


def ok(data: Any, request_id: str | None = None) -> dict[str, Any]:
    return {
        "success": True,
        "data": data,
        "meta": {"request_id": request_id or get_request_id()},
    }


def err(
    code: str, message: str, request_id: str | None = None, details: Any = None
) -> dict[str, Any]:
    error: dict[str, Any] = {
        "code": code,
        "message": message,
        "request_id": request_id or get_request_id(),
    }
    if details is not None:
        error["details"] = details
    return {"success": False, "error": error}
