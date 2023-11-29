from pytest import raises
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from src.app.models import db
from src.app.models.users import User
from src.app.schemas.roles import RoleSchema, Role


def test_roles_schema_load(populate_db):
    role = RoleSchema().load({"name": "role", "users": [1]})

    assert isinstance(role, Role)
    assert role.id is None
    assert role.name == "role"
    assert all(map(lambda u: isinstance(u, User), role.users))


def test_roles_schema_dump(populate_db):
    role = db.session.get(Role, 1)
    dump = RoleSchema().dump(role)

    assert isinstance(dump, dict)
    assert dump["id"] == 1
    assert dump["name"] == "admin"
    assert all(map(lambda u: isinstance(u, int), dump["users"]))


def test_roles_schema_not_unique_name(populate_db):
    with raises(ValidationError) as exc:
        RoleSchema().load({"name": "admin", "users": [1]})
    assert "Name must be unique" in str(exc.value)


def test_roles_schema_name_min_length():
    with raises(ValidationError) as exc:
        RoleSchema().load({"name": "ab", "users": []})
    assert "Length must be between 3 and 50" in str(exc.value)


def test_roles_schema_user_not_found(populate_db):
    with raises(NotFound) as exc:
        RoleSchema().load({"name": "role", "users": [3]})
    assert "User 3 not found" in str(exc.value)
