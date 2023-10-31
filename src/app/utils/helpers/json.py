from flask import jsonify

from src.app.logger import get_logger

log = get_logger(__name__)


def jsonify_success_response(status_code: int = 200):
    return jsonify({"status": "success"}), status_code


def jsonify_error_response(status_code: int, name: str, message: str):
    data = dict(status_code=status_code, name=name, message=message)
    log.debug(f"Exception handled. Returning response: {data}")
    return jsonify(data), status_code
