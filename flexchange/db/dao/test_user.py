import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from flexchange.db.dao.user import User as UserDAO
from flexchange.db.models.user import User as UserModel

create_user_fields = {
    "full_name": "Gendo Ikari",
    "email": "ikari@nerv.jp",
    "password": "gendowned",
    "is_superuser": True,
}
new_user_fields = {
    "id": 1,
    "full_name": create_user_fields["full_name"],
    "email": create_user_fields["email"],
    "hashed_password": f"hashed_{create_user_fields['password']}",
    "is_superuser": create_user_fields["is_superuser"],
}


@pytest.mark.anyio
async def test_create(user_dao: UserDAO, monkeypatch) -> None:
    with monkeypatch.context() as m:
        m.setattr("flexchange.db.dao.user.get_password_hash", lambda x: f"hashed_{x}")
        new_user = await user_dao.create(**create_user_fields)

    assert new_user is not None
    assert new_user.full_name == create_user_fields["full_name"]
    assert new_user.email == create_user_fields["email"]
    assert new_user.hashed_password == f"hashed_{create_user_fields['password']}"
    assert new_user.is_superuser is True


@pytest.mark.anyio
async def test_get(
    user_dao: UserDAO,
    existing_user,
) -> None:
    user_from_db = await user_dao.get(user_id=1)

    assert user_from_db is not None
    for field in new_user_fields:
        assert getattr(user_from_db, field) == new_user_fields[field]


@pytest.mark.anyio
async def test_get_by_email(
    user_dao: UserDAO,
    existing_user,
) -> None:
    user_from_db = await user_dao.get_by_email(email=new_user_fields["email"])

    assert user_from_db is not None
    for field in new_user_fields:
        assert getattr(user_from_db, field) == new_user_fields[field]


@pytest.mark.anyio
async def test_authenticate_succeeds(user_dao: UserDAO, existing_user, monkeypatch) -> None:
    with monkeypatch.context() as m:
        m.setattr("flexchange.db.dao.user.verify_password", lambda x, y: True)
        user_from_db = await user_dao.authenticate(
            email=create_user_fields["email"],
            password=create_user_fields["password"],
        )

    assert user_from_db is not None
    for field in new_user_fields:
        assert getattr(user_from_db, field) == new_user_fields[field]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "email",
    ["shinji@nerv.jp", new_user_fields["email"]],
    ids=("user not found", "wrong password"),
)
async def test_authenticate_fails(email, user_dao: UserDAO, existing_user, monkeypatch) -> None:
    with monkeypatch.context() as m:
        m.setattr("flexchange.db.dao.user.verify_password", lambda x, y: False)
        user_from_db = await user_dao.authenticate(email=email, password=create_user_fields["password"])

    assert user_from_db is None


@pytest.fixture
async def existing_user(dbsession: AsyncSession):
    dbsession.add(UserModel(**new_user_fields))
    await dbsession.commit()


@pytest.fixture
def user_dao(dbsession: AsyncSession):
    return UserDAO(dbsession)
