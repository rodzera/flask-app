from enum import Enum
from functools import wraps
from flask import abort, request

from src.app.logger import get_logger


log = get_logger(__name__)


def log_json_after_request(response):
    if response.get_json():
        log.debug(f"Returning response: {response.json}")
    return response


class Mimetypes(Enum):
    json = "application/json"
    form = "application/x-www-form-urlencoded"


def request_validator(mimetype: str = "json", content_type: bool = False):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            log.debug({
                "request": {
                    "endpoint": request.endpoint,
                    "method": request.method,
                    "headers": request.headers,
                }
            })

            if not hasattr(Mimetypes, mimetype):
                log.exception(f"Mimetype not implemented: {mimetype}")
                abort(501)

            if not request.accept_mimetypes[getattr(Mimetypes, mimetype).value]:
                log.error("Invalid accept headers in the request")
                abort(406)

            if not content_type:
                return func(*args, **kwargs)

            data = False
            if mimetype == "json":
                data = request.get_json(silent=True)
                if not data:
                    abort(400, "Missing json data")
            elif mimetype == "form":
                data = request.form

            log.debug(f"Request content-type in headers: {request.content_type}")
            log.debug(f"Request data: {data}") if data else log.debug("No request data")

            if not data:
                log.error("Invalid content-type in request headers")
                abort(400, f"Invalid content-type, this resource only accept: {getattr(Mimetypes, mimetype).value}")
            return func(*args, **kwargs)
        return wrap
    return decorator
