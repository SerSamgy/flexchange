from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from flexchange.db.base import Base


class User(Base):
    """Represents user that could work in system."""

    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name = mapped_column(String(length=256), nullable=False)
    email = mapped_column(String(length=255), index=True, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    is_superuser = mapped_column(Boolean, default=False, nullable=False)

    trader: Mapped["Trader"] = relationship(back_populates="user", lazy="selectin")
