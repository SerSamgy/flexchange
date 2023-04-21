from fastapi.routing import APIRouter

from flexchange.web.api import trades

api_router = APIRouter()
# api_router.include_router(monitoring.router)
# api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(trades.router, prefix="/trades", tags=["trades"])
