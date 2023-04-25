from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship  # pyright: ignore [reportGeneralTypeIssues]
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from flexchange.db.base import Base

if TYPE_CHECKING:
    from flexchange.db.models import Trader


class User(Base):
    """Represents user that could work in system."""

    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name = mapped_column(String(length=256), nullable=False)
    email = mapped_column(String(length=255), index=True, nullable=False, unique=True)
    hashed_password = mapped_column(String, nullable=False)
    is_superuser = mapped_column(Boolean, default=False, nullable=False)

    trader: Mapped["Trader"] = relationship(
        back_populates="user",
        lazy="selectin",
    )
