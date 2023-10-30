from flask import request, jsonify
from logging import getLevelName

from src.app.logger import get_logger
from src.app.resources.api import api
from src.app.utils import api_auth
from src.app.utils.handlers.request import request_validator
from src.app.schemas.settings import LoggerLevelSchema

log = get_logger(__name__)


@api.route("/settings/logs", methods=["GET"])
@request_validator()
@api_auth(roles=["admin"])
def get_logger_level():
    return {"level": getLevelName(log.level)}, 200


@api.route("/settings/logs", methods=["PUT"])
@request_validator(content_type=True)
@api_auth(roles=["admin"])
def set_logger_level():
    LoggerLevelSchema().load(request.json)
    return jsonify(request.json)
