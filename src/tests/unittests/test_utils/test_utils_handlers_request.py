from flask import Response
from pytest import raises
from unittest.mock import MagicMock
from werkzeug.exceptions import NotImplemented, NotAcceptable, BadRequest

from src.app.utils import log_json_after_request, request_validator
from src.tests.unittests.utils import _func, mocked_payload, headers


def test_log_json_after_request():
    mocked_response = MagicMock(spec=Response)
    response = log_json_after_request(mocked_response)

    assert response == mocked_response
    mocked_response.get_json.assert_called_once()


def test_request_validator_without_payload(ctx):
    with ctx.test_request_context("/route",  headers=headers()):
        result = request_validator()(_func)()
        assert result == "returned"


def test_request_validator_with_payload(ctx):
    with ctx.test_request_context("/route", method="POST", json=mocked_payload, headers=headers()):
        result = request_validator()(_func)()
        assert result == "returned"


def test_request_validator_501(ctx):
    with ctx.test_request_context("/route", method="POST", mimetype="multipart/form-data", headers=headers()):
        with raises(NotImplemented) as exc:
            request_validator()(_func)()
        assert "Not Implemented" in str(exc.value)


def test_request_validator_406(ctx):
    with ctx.test_request_context("/route", method="POST", json=mocked_payload):
        with raises(NotAcceptable) as exc:
            request_validator()(_func)()
        assert "Not Acceptable" in str(exc.value)


def test_request_validator_400(ctx):
    with ctx.test_request_context("/route", method="POST", headers=headers(**{"Content-Type": "application/json"})):
        with raises(BadRequest) as exc:
            request_validator()(_func)()
        assert "Bad Request" in str(exc.value)
