from datetime import datetime

import pytest
from parsel import Selector
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from flexchange.db.dao import Trade as TradeDAO
from flexchange.db.dao import User as UserDAO
from flexchange.db.models import Directions
from flexchange.db.models import Trader as TraderModel
from flexchange.web.api.dependencies import get_current_user_trader

trader_id = "eva_02"
today = datetime.now().date()


@pytest.mark.anyio
async def test_get_pnl_report_no_trades(fastapi_app_overridden, client):
    url = fastapi_app_overridden.url_path_for("get_pnl_report")
    response = await client.get(url)
    report_page = response.text

    assert response.status_code == status.HTTP_200_OK

    selector = Selector(report_page)
    page_title = selector.xpath("//title/text()")
    assert page_title.get() == f"PnL for {trader_id} on {today.strftime('%d %B %Y')}"
    body_p = selector.xpath("//body/p/text()")
    assert body_p.get() == "There're no trades so far!"


@pytest.mark.anyio
async def test_get_pnl_report_with_trades(fastapi_app_overridden, client, trade_dao):
    await trade_dao.create(
        id="trade_02_1",
        trader_id=trader_id,
        price=50,
        quantity=5,
        direction=Directions.buy,
        delivery_day=today,
        delivery_hour=13,
        execution_time=datetime.now(),
    )
    await trade_dao.create(
        id="trade_02_2",
        trader_id=trader_id,
        price=55,
        quantity=6,
        direction=Directions.sell,
        delivery_day=today,
        delivery_hour=13,
        execution_time=datetime.now(),
    )
    await trade_dao.create(
        id="trade_02_3",
        trader_id=trader_id,
        price=58,
        quantity=4,
        direction=Directions.sell,
        delivery_day=today,
        delivery_hour=13,
        execution_time=datetime.now(),
    )
    await trade_dao.create(
        id="trade_02_4",
        trader_id=trader_id,
        price=50,
        quantity=7,
        direction=Directions.buy,
        delivery_day=today,
        delivery_hour=17,
        execution_time=datetime.now(),
    )
    await trade_dao.create(
        id="trade_02_5",
        trader_id=trader_id,
        price=55,
        quantity=2,
        direction=Directions.sell,
        delivery_day=today,
        delivery_hour=17,
        execution_time=datetime.now(),
    )

    url = fastapi_app_overridden.url_path_for("get_pnl_report")
    response = await client.get(url)
    report_page = response.text

    assert response.status_code == status.HTTP_200_OK

    selector = Selector(report_page)
    table_rows = selector.xpath("//tr")
    assert len(table_rows) == 4  # first line - headers, next 2 - pnl records, last - total pnl
    # each 5 consecutive values represent one row
    expected_tr_values = [
        "13",
        "3",
        "5",
        "10",
        "312",
        "17",
        "2",
        "7",
        "2",
        "-240",
        "Total",
        "5",
        "12",
        "12",
        "72",
    ]
    assert table_rows.xpath("td/text()").getall() == expected_tr_values


@pytest.fixture
def fastapi_app_overridden(fastapi_app, user_trader):
    fastapi_app.dependency_overrides[get_current_user_trader] = lambda: user_trader
    yield fastapi_app
    fastapi_app.dependency_overrides = {}


@pytest.fixture
async def user_trader(dbsession):
    user_dao = UserDAO(dbsession)
    new_user = await user_dao.create(
        full_name="Asuka Langley Soryu",
        email="asuka.langley.soryu@nerv.de",
        password="gendowned",
        is_superuser=False,
    )
    dbsession.add(TraderModel(id=trader_id, user_id=new_user.id))
    await dbsession.commit()
    await dbsession.refresh(new_user)

    return new_user


@pytest.fixture
def trade_dao(dbsession: AsyncSession):
    return TradeDAO(dbsession)
