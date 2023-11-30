from unittest.mock import call

from src.app.models.users import User
from src.app.models.roles import Role, create_default_roles


def test_role_model():
    user = User(username="test", password="password")
    role = Role(name="test", users=[user])

    assert Role.DEFAULT_ROLES == ("admin", "user")
    assert role.name == "test"
    assert user in role.users


def test_create_default_roles(mocker, runner):
    mocked_model = mocker.patch("src.app.models.roles.Role")
    mocked_model.DEFAULT_ROLES = Role.DEFAULT_ROLES
    mocked_model.query.filter_by.return_value.first.return_value = None

    create_default_roles()

    mocked_model.query.filter_by.assert_has_calls(
        [call(name="admin"), call().first(), call(name="user"), call().first()]
    )
    mocked_model.assert_has_calls(
        [call(name="admin"), call(name="user")],
        any_order=True
    )
    mocked_model.return_value.orm_handler.assert_has_calls(
        [call("add"), call("add")]
    )
