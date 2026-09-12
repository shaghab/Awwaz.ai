from fastapi import APIRouter

from app.api.routes import admin, auth
from app.core.config import Settings


def build_api_router(settings: Settings) -> APIRouter:
    """Assemble the versioned API surface.

    Demo routes are mounted only when demo mode is on. Gating them with a
    dependency is not enough on its own: a registered route answers an
    undeclared verb with 405 during routing, before any dependency runs, which
    tells a prober the route is there (PRD §12).
    """
    api_router = APIRouter(prefix="/api/v1")
    api_router.include_router(auth.router)

    if settings.AWWAZ_DEMO_MODE:
        api_router.include_router(auth.demo_router)
        api_router.include_router(admin.demo_router)

    return api_router
