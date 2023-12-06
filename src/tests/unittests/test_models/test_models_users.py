from src.app.models.base import BaseModel
from src.app.models.roles import Role
from src.app.models.users import User
from src.app.schemas.users import UserSchema


def test_user_class():
    issubclass(User, BaseModel)


def test_user_attributes():
    hasattr(Role, "username")
    hasattr(Role, "password")
    hasattr(Role, "roles")


def test_user_schema():
    isinstance(User.schema(), UserSchema)


def test_user_init(mocker):
    mocked_method = mocker.patch.object(User, "orm")
    mocker.patch.object(Role, "orm")

    role = Role(name="test")
    user = User(username="test", password="password", roles=[role])
    mocked_method.assert_called_once_with("add")

    assert user.username == "test"
    assert user.password != "password"
    assert user.check_password("password") is True
    assert role in user.roles
