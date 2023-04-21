from fastapi.routing import APIRouter

from flexchange.web.api import login, monitoring, trades

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(login.router, tags=["login"])
api_router.include_router(trades.router, prefix="/trades", tags=["trades"])
