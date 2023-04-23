from typing import Any

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from flexchange.db.dependencies import get_db_session
from flexchange.db.models.user import User as UserModel
from flexchange.security import get_password_hash, verify_password


class User:
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create(self, **obj_fields: Any) -> UserModel:
        db_obj = UserModel(
            full_name=obj_fields["full_name"],
            email=obj_fields["email"],
            hashed_password=get_password_hash(obj_fields["password"]),
            is_superuser=obj_fields["is_superuser"],
        )
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

        return db_obj

    async def get(self, *, user_id: int) -> UserModel | None:
        return await self.session.get(UserModel, user_id)

    async def get_by_email(self, *, email: str) -> UserModel | None:
        rows = await self.session.execute(
            select(UserModel).where(UserModel.email == email),
        )
        return rows.scalars().first()

    async def authenticate(self, *, email: str, password: str) -> UserModel | None:
        user = await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        return user
