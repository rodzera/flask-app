from pytest import raises
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from src.app.models.users import User
from src.app.models.roles import Role


def test_schemas_roles_load():
    user = User(username="user", password="user")
    role = Role.schema().load({"name": "role", "users": [user.id]})

    assert isinstance(role, Role)
    assert role.id == 1
    assert role.name == "role"
    assert user in role.users


def test_schemas_roles_dump():
    user = User(username="user", password="user")
    role = Role(name="role", users=[user])
    dump = Role.schema().dump(role)

    assert isinstance(dump, dict)
    assert dump["id"] == 1
    assert dump["name"] == "role"
    assert user.id in dump["users"]


def test_schemas_roles_not_unique_name():
    Role(name="role")
    with raises(ValidationError) as exc:
        Role.schema().load({"name": "role", "users": []})
    assert "Name must be unique" in str(exc.value)


def test_schemas_roles_min_name_length():
    with raises(ValidationError) as exc:
        Role.schema().load({"name": "ab", "users": []})
    assert "Length must be between 3 and 50" in str(exc.value)


def test_schemas_roles_user_not_found():
    User(username="user", password="password")
    with raises(NotFound) as exc:
        Role.schema().load({"name": "role", "users": [3]})
    assert "User 3 not found" in str(exc.value)
