from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String

from flexchange.db.base import Base


class Trader(Base):
    """Represents actor who deals with trades."""

    __tablename__ = "trader"

    id = mapped_column(String(length=64), primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    # if trader is bot we could add another foreign key to Bot table
    # and add constraint that checks if either one of foreign keys
    # references to respective table, but not both

    user: Mapped["User"] = relationship(back_populates="trader")  # pyright: ignore [reportUndefinedVariable]
