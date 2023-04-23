from datetime import date
from typing import Any

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from flexchange.db.dependencies import get_db_session
from flexchange.db.models import Trade as TradeModel


class Trade:
    """Class for accessing trade table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(self, **kwargs: Any) -> None:
        """
        Add single trade to session.

        :param kwargs: new trade's fields.
        """
        self.session.add(TradeModel(**kwargs))

    async def filter(
        self,
        trader_id: str | None = None,
        delivery_day: date | None = None,
    ) -> list[TradeModel]:
        """
        Get specific trade models.

        :param trader_id: ID of trader, responsible for trade.
        :param delivery_day: Day on which the traded energy has to be delivered.
        :return: (filtered) trade models.
        """
        query = select(TradeModel)
        if trader_id:
            query = query.where(TradeModel.trader_id == trader_id)
        if delivery_day:
            query = query.where(TradeModel.delivery_day == delivery_day)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
