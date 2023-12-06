from unittest.mock import call

from src.app.models.base import BaseModel
from src.app.models.users import User
from src.app.models.roles import Role
from src.app.schemas.roles import RoleSchema


def test_role_class():
    issubclass(Role, BaseModel)


def test_role_attributes():
    hasattr(Role, "name")
    hasattr(Role, "users")
    hasattr(Role, "DEFAULT_ROLES")


def test_role_schema():
    isinstance(Role.schema(), RoleSchema)


def test_role_model(mocker):
    mocked_method = mocker.patch.object(Role, "orm")
    mocker.patch.object(User, "orm")

    user = User(username="test", password="password")
    role = Role(name="test", users=[user])
    mocked_method.assert_called_once_with("add")

    assert role.name == "test"
    assert user in role.users
    assert Role.DEFAULT_ROLES == ("admin", "user")


def test_role_create_default_roles(mocker, runner):
    mocked_init = mocker.patch.object(Role, "__init__")
    mocked_w_entities = mocker.patch.object(Role, "w_entities")
    mocked_init.return_value = None
    mocked_w_entities.return_value.first.return_value = None

    Role.create_default_roles()
    mocked_init.assert_has_calls([
        call(name="admin"), call(name="user")
    ])
    mocked_w_entities.assert_has_calls([
        call("name", name="admin"),
        call().first(),
        call("name", name="user"),
        call().first()
    ])
