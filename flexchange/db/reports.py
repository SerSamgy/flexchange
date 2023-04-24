from datetime import date, datetime

from fastapi import Depends
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from flexchange.db.dependencies import get_db_session
from flexchange.db.models import Trade as TradeModel


class PnLReport:
    """Class for fetching of data to generate PnL (Profit & Loss) report."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> list[dict]:
        self.session = session

    async def generate_for_day(self, *, trader_id: str, delivery_day: date | None = None):
        """Fetches all fields for report filtered by `trader_id` and `delivery_date`."""
        if not delivery_day:
            delivery_day = datetime.now().date()

        query = (
            select(
                TradeModel.delivery_hour,
                func.count("*").label("num_of_trades"),
                func.coalesce(
                    func.sum(case((TradeModel.direction == "buy", TradeModel.quantity), else_=0)),
                    0,
                ).label("total_buy"),
                func.coalesce(
                    func.sum(case((TradeModel.direction == "sell", TradeModel.quantity), else_=0)),
                    0,
                ).label("total_sell"),
                func.coalesce(
                    func.sum(
                        case(
                            (TradeModel.direction == "sell", TradeModel.quantity * TradeModel.price),
                            else_=-TradeModel.quantity * TradeModel.price,
                        ),
                    ),
                    0,
                ).label("pnl"),
            )
            .filter_by(trader_id=trader_id, delivery_day=delivery_day)
            .group_by(TradeModel.delivery_day, TradeModel.delivery_hour)
        )
        rows = await self.session.execute(query)

        return rows.mappings().all()
