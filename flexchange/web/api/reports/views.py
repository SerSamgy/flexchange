from datetime import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from flexchange.db.models import User as UserModel
from flexchange.db.reports import PnLReport
from flexchange.web.api.dependencies import get_current_user_trader
from flexchange.web.templates import templates

router = APIRouter()


@router.get("/pnl", response_class=HTMLResponse)
async def get_pnl_report(
    request: Request,
    current_user: UserModel = Depends(get_current_user_trader),
    pnl_report: PnLReport = Depends(),
):
    """Generate PnL report for current user trader for today. Only traders can access this endpoint."""
    trader_id = current_user.trader.id
    delivery_day = datetime.now().date()
    pnl_records = await pnl_report.generate_for_day(trader_id=trader_id, delivery_day=delivery_day)

    return templates.TemplateResponse(
        "pnl_daily.html",
        {
            "request": request,
            "trader_id": trader_id,
            "delivery_day": delivery_day,
            "pnl_records": pnl_records,
        },
    )
