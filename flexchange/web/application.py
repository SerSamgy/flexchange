from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from flexchange.settings import settings
from flexchange.web.api.router import api_router
from flexchange.web.lifetime import register_shutdown_event, register_startup_event


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="flexchange",
        version=metadata.version("flexchange"),
        docs_url=f"{settings.api_str}/docs",
        redoc_url=f"{settings.api_str}/redoc",
        openapi_url=f"{settings.api_str}/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix=settings.api_str)

    return app
