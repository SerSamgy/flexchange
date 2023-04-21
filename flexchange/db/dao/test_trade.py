from datetime import date, datetime
from typing import Coroutine

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from flexchange.db.dao.trade import Trade as TradeDAO
from flexchange.db.models.trade import Trade as TradeModel
from flexchange.db.models.trader import Trader as TraderModel


@pytest.mark.anyio
async def test_create(
    dbsession: AsyncSession,
    trade_dao: TradeDAO,
    existing_trader: Coroutine[None, None, None],
) -> None:
    """Tests trade instance creation."""
    delivery_day = date(2023, 4, 20)
    execution_time = datetime(2023, 4, 20, 10, 5, 11, 123)
    create_fields = {
        "id": "trade_1",
        "trader_id": "MirkoT",
        "price": 50,
        "quantity": 10,
        "direction": "buy",
        "delivery_day": delivery_day,
        "delivery_hour": 12,
        "execution_time": execution_time,
    }
    await trade_dao.create(**create_fields)

    saved_obj = await dbsession.get(TradeModel, create_fields["id"])
    assert saved_obj is not None
    assert saved_obj.trader_id == create_fields["trader_id"]
    assert saved_obj.price == create_fields["price"]
    assert saved_obj.quantity == create_fields["quantity"]
    assert saved_obj.direction == create_fields["direction"]
    assert saved_obj.delivery_day == create_fields["delivery_day"]
    assert saved_obj.delivery_hour == create_fields["delivery_hour"]
    assert saved_obj.execution_time == create_fields["execution_time"]


@pytest.fixture
def trade_dao(dbsession: AsyncSession):
    return TradeDAO(dbsession)


@pytest.fixture
async def existing_trader(dbsession: AsyncSession) -> Coroutine[None, None, None]:
    dbsession.add(TraderModel(id="MirkoT", type="human"))
    await dbsession.commit()
