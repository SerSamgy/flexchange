from datetime import date, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from flexchange.db.dao.trade import Trade as TradeDAO
from flexchange.db.models.trade import Trade as TradeModel
from flexchange.db.models.trader import Trader as TraderModel


@pytest.mark.anyio
async def test_create(
    dbsession: AsyncSession,
    trade_dao: TradeDAO,
) -> None:
    """Tests trade instance creation."""
    dbsession.add(TraderModel(id="MirkoT", type="human"))
    await dbsession.commit()
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


@pytest.mark.anyio
async def test_filter(
    dbsession: AsyncSession,
    trade_dao: TradeDAO,
) -> None:
    """Tests fetch of trade objects filtered by given fields."""
    trader_1 = TraderModel(id="ReiAya", type="human")
    trader_2 = TraderModel(id="AsukaSor", type="human")
    dbsession.add(trader_2)
    dbsession.add(trader_1)
    await dbsession.commit()

    delivery_day_1 = date(2023, 4, 20)
    trade_1 = TradeModel(
        id="trade_1",
        trader_id=trader_1.id,
        price=50,
        quantity=10,
        direction="buy",
        delivery_day=delivery_day_1,
        delivery_hour=12,
        execution_time=datetime(2023, 4, 20, 10, 5, 11, 123),
    )
    dbsession.add(trade_1)

    delivery_day_2 = date(2023, 4, 21)
    trade_2 = TradeModel(
        id="trade_2",
        trader_id=trader_2.id,
        price=50,
        quantity=10,
        direction="buy",
        delivery_day=delivery_day_2,
        delivery_hour=12,
        execution_time=datetime(2023, 4, 21, 10, 5, 11, 123),
    )
    dbsession.add(trade_2)

    # no filter
    trades = await trade_dao.filter()
    assert len(trades) == 2
    assert trades[0].id == trade_1.id
    assert trades[1].id == trade_2.id

    # filter by trader_id
    trades = await trade_dao.filter(trader_id=trader_2.id)
    assert len(trades) == 1
    assert trades[0].id == trade_2.id

    # filter by delivery_day
    trades = await trade_dao.filter(delivery_day=trade_1.delivery_day)
    assert len(trades) == 1
    assert trades[0].id == trade_1.id


@pytest.fixture
def trade_dao(dbsession: AsyncSession):
    return TradeDAO(dbsession)
