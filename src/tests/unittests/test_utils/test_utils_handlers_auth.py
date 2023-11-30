from pytest import raises
from unittest.mock import MagicMock
from werkzeug.exceptions import Unauthorized

from src.app.utils import authenticate, api_auth
from src.tests.unittests.utils import headers, user_auth, _func


def test_authenticate_function(mocker):
    admin = authenticate("admin", "admin")
    assert admin == ["admin"]

    mocked_model = mocker.patch("src.app.utils.handlers.auth.User")
    mocked_user = mocked_model.query.filter_by.return_value.first.return_value
    mocked_user.check_password.return_value = True
    r1, r2 = MagicMock(), MagicMock()
    r1.name = "user"
    r2.name = "admin"
    mocked_user.roles = [r1, r2]

    user = authenticate("user", "password")
    assert user == ["user", "admin"]
    mocked_model.query.filter_by.assert_called_once_with(username="user")
    mocked_model.query.filter_by.return_value.first.assert_called_once()
    mocked_user.check_password.assert_called_once_with("password")

    mocked_user.check_password.return_value = False
    false = authenticate("test", "test")
    assert false is False


def test_api_auth_decorator_success(ctx, mocker):
    mocked_authentication = mocker.patch("src.app.utils.handlers.auth.authenticate")
    mocked_authentication.return_value = ["admin"]

    with ctx.test_request_context("/route", headers=headers(**user_auth)):
        result = api_auth()(_func)()
        assert result == "returned"
        mocked_authentication.assert_called_once_with("user", "user")


def test_api_auth_decorator_invalid_headers(ctx):
    with ctx.test_request_context("/route", headers=headers()):
        with raises(Unauthorized) as exc:
            api_auth()(_func)()
        assert "Unauthorized" in str(exc.value)


def test_api_auth_decorator_invalid_auth(ctx, mocker):
    mocked_authentication = mocker.patch("src.app.utils.handlers.auth.authenticate")
    mocked_authentication.return_value = False

    with ctx.test_request_context("/route", headers=headers(**user_auth)):
        with raises(Unauthorized) as exc:
            api_auth()(_func)()
        assert "Unauthorized" in str(exc.value)


def test_api_auth_decorator_invalid_role(ctx, mocker):
    mocked_authentication = mocker.patch("src.app.utils.handlers.auth.authenticate")
    mocked_authentication.return_value = ["user"]

    with ctx.test_request_context("/route", headers=headers(**user_auth)):
        with raises(Unauthorized) as exc:
            api_auth()(_func)()
        assert "Unauthorized" in str(exc.value)
