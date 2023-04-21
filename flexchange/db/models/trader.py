import enum

from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.sqltypes import Enum, String

from flexchange.db.base import Base


class TraderTypes(str, enum.Enum):
    bot = "bot"
    human = "human"


class Trader(Base):
    """Represents actor who deals with trades."""

    __tablename__ = "trader"

    id = mapped_column(String(length=64), primary_key=True)
    type = mapped_column(Enum(TraderTypes), nullable=False)  # noqa: WPS432
