from datetime import date

from fastapi import APIRouter
from fastapi.param_functions import Depends

from flexchange.db.dao.trade import Trade as TradeDAO
from flexchange.db.models.trade import Trade as TradeModel
from flexchange.web.api.trades.schema import TradeModelDTO

router = APIRouter()


@router.get("/", response_model=list[TradeModelDTO])
async def get_trades(
    trader_id: str | None = None,
    delivery_day: date | None = None,
    trade_dao: TradeDAO = Depends(),
) -> list[TradeModel]:
    """Retrieve trade objects from the database."""
    return await trade_dao.filter(trader_id=trader_id, delivery_day=delivery_day)


@router.post("/")
async def create_trade(
    new_trade_object: TradeModelDTO,
    trade_dao: TradeDAO = Depends(),
) -> None:
    """Creates trade model in the database."""
    await trade_dao.create(**new_trade_object.dict())
