from datetime import date, datetime

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from flexchange.db.dao.trade import Trade as TradeDAO
from flexchange.db.models.trader import Trader as TraderModel

trader_1_id = "ReiAya"
trade_1_id = "trade_1"
trade_1 = {
    "id": trade_1_id,
    "trader_id": trader_1_id,
    "price": 50,
    "quantity": 10,
    "direction": "buy",
    "delivery_day": date(2023, 4, 20),
    "delivery_hour": 12,
    "execution_time": datetime(2023, 4, 20, 10, 5, 11, 123),
}
trade_1_json = trade_1 | {
    "delivery_day": trade_1["delivery_day"].isoformat(),
    "execution_time": trade_1["execution_time"].isoformat(),
}
trade_2 = {
    "id": "trade_2",
    "trader_id": "AsukaSor",
    "price": 55,
    "quantity": 100,
    "direction": "sell",
    "delivery_day": date(2023, 4, 21),
    "delivery_hour": 22,
    "execution_time": datetime(2023, 4, 21, 10, 5, 11, 123),
}
trade_2_json = trade_2 | {
    "delivery_day": trade_2["delivery_day"].isoformat(),
    "execution_time": trade_2["execution_time"].isoformat(),
}


@pytest.mark.anyio
async def test_create_trade(
    fastapi_app: FastAPI,
    client: AsyncClient,
    trade_dao,
) -> None:
    """Tests trade instance creation."""
    url = fastapi_app.url_path_for("create_trade")
    response = await client.post(url, json=trade_1_json)

    assert response.status_code == status.HTTP_200_OK
    instances = await trade_dao.filter(trader_id=trader_1_id)
    assert instances[0].id == trade_1_id


@pytest.mark.anyio
@pytest.mark.parametrize(
    "query, output",
    [
        ({}, [trade_1_json, trade_2_json]),
        ({"trader_id": trader_1_id}, [trade_1_json]),
        ({"delivery_day": trade_2_json["delivery_day"]}, [trade_2_json]),
    ],
    ids=["no filter", "filter by trader_id", "filter by delivery_day"],
)
async def test_get_trades(
    fastapi_app: FastAPI,
    client: AsyncClient,
    trade_dao: TradeDAO,
    query,
    output,
) -> None:
    """Tests trade instances retrieval."""
    await trade_dao.create(**trade_1)
    await trade_dao.create(**trade_2)

    url = fastapi_app.url_path_for("get_trades")
    response = await client.get(url, params=query)
    trades = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert trades == output


@pytest.fixture
def trade_dao(dbsession: AsyncSession):
    return TradeDAO(dbsession)


@pytest.fixture(autouse=True)
async def db_state(dbsession):
    dbsession.add(TraderModel(id=trader_1_id, type="human"))
    dbsession.add(TraderModel(id="AsukaSor", type="human"))
    await dbsession.commit()
