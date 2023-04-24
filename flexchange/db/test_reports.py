from datetime import datetime, timedelta, timezone

import pytest

from flexchange.db.models import Directions
from flexchange.db.models import Trade as TradeModel
from flexchange.db.models import Trader as TraderModel
from flexchange.db.reports import PnLReport

today_delivery = datetime.now(timezone.utc).date()


@pytest.mark.anyio
@pytest.mark.parametrize(
    "delivery_day",
    [today_delivery, None],
    ids=["delivery_day defined", "delivery_day undefined"],
)
async def test_pnl_report_generate(delivery_day, dbsession, pnl_report):
    # initialize data
    trader_1 = TraderModel(id="eva_01")
    dbsession.add(trader_1)
    trader_2 = TraderModel(id="eva_02")
    dbsession.add(trader_2)
    await dbsession.commit()
    # must be filtered out because of different `trader_id`
    dbsession.add(
        TradeModel(
            id="trade_02_1",
            trader_id=trader_2.id,
            price=24,
            quantity=5,
            direction=Directions.sell,
            delivery_day=today_delivery,
            delivery_hour=8,
        ),
    )
    dbsession.add(
        TradeModel(
            id="trade_01_1",
            trader_id=trader_1.id,
            price=20,
            quantity=10,
            direction=Directions.buy,
            delivery_day=today_delivery,
            delivery_hour=8,
        ),
    )
    dbsession.add(
        TradeModel(
            id="trade_01_2",
            trader_id=trader_1.id,
            price=25,
            quantity=5,
            direction=Directions.sell,
            delivery_day=today_delivery,
            delivery_hour=8,
        ),
    )
    dbsession.add(
        TradeModel(
            id="trade_01_3",
            trader_id=trader_1.id,
            price=20,
            quantity=3,
            direction=Directions.buy,
            delivery_day=today_delivery,
            delivery_hour=12,
        ),
    )
    dbsession.add(
        TradeModel(
            id="trade_01_4",
            trader_id=trader_1.id,
            price=25,
            quantity=9,
            direction=Directions.sell,
            delivery_day=today_delivery,
            delivery_hour=12,
        ),
    )
    # must be filtered out because of different `delivery_day`
    dbsession.add(
        TradeModel(
            id="trade_01_5",
            trader_id=trader_1.id,
            price=30,
            quantity=5,
            direction=Directions.sell,
            delivery_day=today_delivery - timedelta(days=1),
            delivery_hour=12,
        ),
    )

    records = await pnl_report.generate_for_day(trader_id=trader_1.id, delivery_day=delivery_day)

    expected_records = [
        {"delivery_hour": 8, "num_of_trades": 2, "total_buy": 10, "total_sell": 5, "pnl": -75},
        {"delivery_hour": 12, "num_of_trades": 2, "total_buy": 3, "total_sell": 9, "pnl": 165},
    ]
    assert records == expected_records


@pytest.fixture
def pnl_report(dbsession):
    return PnLReport(dbsession)
