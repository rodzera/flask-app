from flask import request, jsonify
from logging import getLevelName

from src.app.logger import get_logger
from src.app.resources.api import api
from src.app.utils import api_auth, request_validator
from src.app.schemas.settings import LoggerLevelSchema

log = get_logger(__name__)

schema = LoggerLevelSchema()


@api.route("/settings/logs", methods=["GET"])
@api_auth(roles=["admin"])
@request_validator()
def get_logger_level():
    return {"level": getLevelName(log.level)}, 200


@api.route("/settings/logs", methods=["PUT"])
@api_auth(roles=["admin"])
@request_validator()
def set_logger_level():
    return jsonify(schema.load(request.json))
