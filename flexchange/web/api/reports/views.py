from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from flexchange.db.reports import PnLReport
from flexchange.web.api.dependencies import get_current_user
from flexchange.web.templates import templates

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/pnl", response_class=HTMLResponse)
async def get_pnl_report(
    request: Request,
    pnl_report: PnLReport = Depends(),
):
    """Generate PnL report for current user trader for today."""
    # FIXME: get trader_id from current user info
    trader_id = "eva_02"
    delivery_day = datetime.now(timezone.utc).date()
    pnl_records = await pnl_report.generate_for_day(trader_id=trader_id, delivery_day=date(2023, 4, 23))
    # TODO: add render of empty table if there're no rows

    return templates.TemplateResponse(
        "pnl_daily.html",
        {
            "request": request,
            "trader_id": trader_id,
            "delivery_day": delivery_day,
            "pnl_records": pnl_records,
        },
    )
