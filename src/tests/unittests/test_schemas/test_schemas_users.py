from pytest import raises
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from src.app.models import db
from src.app.models.roles import Role
from src.app.schemas.users import User, UserSchema


def test_schemas_users_load(populate_db):
    user = UserSchema().load({"username": "test", "password": "password", "roles": [1]})

    assert isinstance(user, User)
    assert user.id is None
    assert user.username == "test"
    assert user.check_password("password")
    assert all(map(lambda r: isinstance(r, Role), user.roles))


def test_schemas_users_dump(populate_db):
    user = db.session.get(User, 1)
    dump = UserSchema().dump(user)

    assert isinstance(dump, dict)
    assert dump["id"] == 1
    assert dump["username"] == "uadmin"
    assert "password" not in dump.keys()
    assert all(map(lambda u: isinstance(u, int), dump["roles"]))


def test_schemas_users_not_unique_username(populate_db):
    with raises(ValidationError) as exc:
        UserSchema().load({"username": "user", "password": "password", "roles": [1]})
    assert "Username must be unique" in str(exc.value)


def test_schemas_users_forbidden_username(populate_db):
    with raises(ValidationError) as exc:
        UserSchema().load({"username": "admin", "password": "password", "roles": [1]})
    assert "Forbidden username" in str(exc.value)


def test_schemas_users_min_username_length(populate_db):
    with raises(ValidationError) as exc:
        UserSchema().load({"username": "ab", "password": "password", "roles": [1]})
    assert "Length must be between 3 and 50" in str(exc.value)


def test_schemas_users_min_password_length(populate_db):
    with raises(ValidationError) as exc:
        UserSchema().load({"username": "test", "password": "pa", "roles": [1]})
    assert "Length must be between 5 and 20" in str(exc.value)


def test_schemas_users_role_not_found(populate_db):
    with raises(NotFound) as exc:
        UserSchema().load({"username": "test", "password": "password", "roles": [3]})
    assert "Role 3 not found" in str(exc.value)
