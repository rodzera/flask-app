from src.app.models.roles import Role
from src.app.models.users import User


def test_role_model():
    user = User(username="test", password="password")
    role = Role(name="test", users=[user])

    assert role.name == "test"
    assert user in role.users
