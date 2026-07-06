"""ASGI application entry point.

This exposes the `app` object that Uvicorn/Gunicorn boots:

    uvicorn main:app --reload

Everything wires together here: typed settings, the versioned API router,
lifespan resource management, CORS, and the auto-generated OpenAPI docs.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.api import api_router
from src.config import Settings, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Async startup/shutdown resource management.

    Code BEFORE `yield` runs once on startup; code AFTER runs on shutdown.
    This is where you open/close shared resources (DB pools, HTTP clients,
    caches) instead of doing it per-request.
    """
    settings = get_settings()

    # --- startup ---
    print(f"Starting {settings.PROJECT_NAME} in '{settings.ENVIRONMENT}' mode")
    # e.g. warm up connection pools, create tables, connect to Redis, etc.

    yield

    # --- shutdown ---
    print(f"Shutting down {settings.PROJECT_NAME}")
    # e.g. dispose the engine, close clients, flush caches, etc.


def create_app() -> FastAPI:
    """Application factory: builds and configures the FastAPI instance."""
    settings: Settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        # Serve the OpenAPI schema (and therefore Swagger UI) under the
        # versioned prefix so v1 and a future v2 never collide.
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS — BACKEND_CORS_ORIGINS is a comma-separated string in .env
    origins = [
        origin.strip()
        for origin in settings.BACKEND_CORS_ORIGINS.split(",")
        if origin.strip()
    ]
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Mount every module router under /api/v1
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/", include_in_schema=False)
    async def root() -> RedirectResponse:
        """Convenience redirect from the root to the interactive docs."""
        return RedirectResponse(url="/docs")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
