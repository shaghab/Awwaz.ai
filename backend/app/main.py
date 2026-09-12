"""FastAPI app factory. Middleware order: request ID -> logging -> error handlers."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.api.routes import health
from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.core.logging import AccessLogMiddleware, configure_logging
from app.core.request_id import RequestIDMiddleware


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging()

    # Disabling only docs_url still leaves /redoc and /openapi.json serving the
    # schema, which lists the demo routes that their 404 gating exists to hide.
    published_docs = settings.AWWAZ_ENV != "prod"

    app = FastAPI(
        title="Awwaz API",
        version="0.1.0",
        docs_url="/docs" if published_docs else None,
        redoc_url="/redoc" if published_docs else None,
        openapi_url="/openapi.json" if published_docs else None,
    )

    # Starlette runs middleware in reverse registration order, so the request ID
    # middleware is added last to make it the outermost layer.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.APP_BASE_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )
    app.add_middleware(AccessLogMiddleware)
    app.add_middleware(RequestIDMiddleware)

    register_error_handlers(app)

    app.include_router(health.router)
    app.include_router(api_router)
    return app


app = create_app()
