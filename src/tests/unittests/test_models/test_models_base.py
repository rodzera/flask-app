from pytest import raises
from werkzeug.exceptions import InternalServerError

from src.app.models import db
from src.app.models.users import User
from src.app.models.roles import Role


def test_orm_handler():
    user = User(username="test", password="password", roles=[])

    user = user.orm_handler("add")
    assert getattr(user, "id")
    assert getattr(user, "created_at")
    assert getattr(user, "updated_on")

    user = user.orm_handler("delete")
    assert db.session.get(User, user.id) is None


def test_orm_handler_rollback(mocker):
    mocked_db = mocker.patch("src.app.models.base.db")
    user = User(username="test", password="password", roles=[])

    mocked_db.session.commit.side_effect = Exception
    with raises(InternalServerError) as exc:
        user.orm_handler("add")
    mocked_db.session.rollback.assert_called_once()
    assert InternalServerError.description in str(exc.value)


def test_update_attrs():
    role = Role(name="test")
    user = User(username="test", password="password", roles=[role])

    user.update_attrs(username="user", roles=[])
    user.set_password("pass")
    assert user.username == "user"
    assert user.password != "pass"
    assert user.check_password("pass") is True
    assert user.roles == []

    with raises(AttributeError) as exc:
        user.update_attrs(password="password")
    assert "Protected attribute" in str(exc.value)
