from flask import Response as FlaskResponse
from werkzeug import Response as WerkezeugResponse
from marshmallow import ValidationError
from werkzeug.exceptions import InternalServerError, NotImplemented

from src.app.utils.handlers.errors import handle_any_error, handle_any_exception

exc = {"status_code": 500, "name": "Internal Server Error", "message": InternalServerError.description}


def test_handle_any_error(ctx):
    response = handle_any_error(InternalServerError())
    assert isinstance(response, WerkezeugResponse)
    assert response.status_code == 500
    assert response.json == exc


def test_handle_any_exception(ctx):
    response = handle_any_exception(InternalServerError)
    assert isinstance(response, FlaskResponse)
    assert response.status_code == 500
    assert response.json == exc

    validation_messages = ["test", "test"]
    response = handle_any_exception(ValidationError(validation_messages, "field"))
    assert isinstance(response, FlaskResponse)
    assert response.status_code == 400
    assert response.json == {"status_code": 400, "name": "Bad Request", "message": validation_messages}

    response = handle_any_exception(Exception())
    assert isinstance(response, FlaskResponse)
    assert response.status_code == 500
    assert response.json == exc
