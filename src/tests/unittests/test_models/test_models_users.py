from src.app.models.roles import Role
from src.app.models.users import User


def test_user_model():
    role = Role(name="test")
    user = User(username="test", password="password", roles=[role])

    assert user.username == "test"
    assert user.password != "password"
    assert user.check_password("password") is True
    assert role in user.roles
