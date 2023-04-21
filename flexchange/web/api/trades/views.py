from datetime import date
from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from flexchange.db.dao.trade import Trade as TradeDAO
from flexchange.db.models.trade import Trade as TradeModel
from flexchange.web.api.trades.schema import DummyModelDTO, DummyModelInputDTO

router = APIRouter()


@router.get("/", response_model=List[DummyModelDTO])
async def get_trades(
    trader_id: str | None,
    delivery_day: date | None,
    trade_dao: TradeDAO = Depends(),
) -> list[TradeModel]:
    """
    Retrieve trade objects from the database.

    :param trader_id: ID of trader, responsible for trade.
    :param delivery_day: Day on which the traded energy has to be delivered.
    :param trade_dao: DAO for trade models.
    :return: list of trade objects from database.
    """
    return await trade_dao.filter(trader_id=trader_id, delivery_day=delivery_day)


@router.post("/")
async def create_trade(
    new_dummy_object: DummyModelInputDTO,
    dummy_dao: TradeDAO = Depends(),
) -> None:
    """
    Creates dummy model in the database.

    :param new_dummy_object: new dummy model item.
    :param dummy_dao: DAO for dummy models.
    """
    await dummy_dao.create_dummy_model(**new_dummy_object.dict())
