from pytest import raises
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from src.app.models.users import User
from src.app.models.roles import Role


def test_schemas_users_load():
    role = Role(name="role")
    user = User.schema().load({"username": "user", "password": "password", "roles": [role.id]})

    assert isinstance(user, User)
    assert user.id == 1
    assert user.username == "user"
    assert user.check_password("password")
    assert role in user.roles


def test_schemas_users_dump():
    role = Role(name="role")
    user = User(username="user", password="user", roles=[role])
    dump = User.schema().dump(user)

    assert isinstance(dump, dict)
    assert dump["id"] == 1
    assert dump["username"] == "user"
    assert "password" not in dump.keys()
    assert role.id in dump["roles"]


def test_schemas_users_not_unique_username():
    User(username="user", password="user")
    with raises(ValidationError) as exc:
        User.schema().load({"username": "user", "password": "password", "roles": []})
    assert "Username must be unique" in str(exc.value)


def test_schemas_users_forbidden_username():
    with raises(ValidationError) as exc:
        User.schema().load({"username": "admin", "password": "password", "roles": []})
    assert "Forbidden username" in str(exc.value)


def test_schemas_users_min_username_length():
    with raises(ValidationError) as exc:
        User.schema().load({"username": "ab", "password": "password", "roles": []})
    assert "Length must be between 3 and 50" in str(exc.value)


def test_schemas_users_min_password_length():
    with raises(ValidationError) as exc:
        User.schema().load({"username": "test", "password": "pa", "roles": []})
    assert "Length must be between 5 and 20" in str(exc.value)


def test_schemas_users_role_not_found():
    with raises(NotFound) as exc:
        User.schema().load({"username": "test", "password": "password", "roles": [1]})
    assert "Role 1 not found" in str(exc.value)
