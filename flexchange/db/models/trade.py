import enum

from sqlalchemy.orm import mapped_column
from sqlalchemy.schema import CheckConstraint, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import Date, DateTime, Enum, Integer, String

from flexchange.db.base import Base


class Directions(str, enum.Enum):
    buy = "buy"
    sell = "sell"


class Trade(Base):
    """Represents match of buy and sell orders."""

    __tablename__ = "trade"

    id = mapped_column(String(length=64), primary_key=True)
    trader_id = mapped_column(ForeignKey("trader.id"))
    price = mapped_column(Integer, nullable=False)  # noqa: WPS432
    quantity = mapped_column(Integer, nullable=False)  # noqa: WPS432
    direction = mapped_column(Enum(Directions), nullable=False)  # noqa: WPS432
    delivery_day = mapped_column(Date, nullable=False)  # noqa: WPS432
    delivery_hour = mapped_column(
        Integer,
        CheckConstraint("delivery_hour >= 0 AND delivery_hour <= 23"),
        nullable=False,
    )  # noqa: WPS432
    execution_time = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=current_timestamp(),
    )  # noqa: WPS432
