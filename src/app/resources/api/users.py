from flask import request, jsonify

from src.app.logger import get_logger
from src.app.resources.api import api
from src.app.models.users import User
from src.app.utils import api_auth, request_validator


log = get_logger(__name__)


@api.route("/users", methods=["GET"])
@api_auth(roles=["admin"])
@request_validator()
def get_users():
    return jsonify({"users": User.dump_all()}), 200


@api.route("/users/<int:user_id>", methods=["GET"])
@api_auth(roles=["admin"])
@request_validator()
def get_user(user_id):
    return jsonify(User.dump(user_id)), 200


@api.route("/users", methods=["POST"])
@api_auth(roles=["admin"])
@request_validator()
def post_user():
    return jsonify(User.load(**request.json).self_dump()), 201


@api.route("/users/<int:user_id>", methods=["PUT"])
@api_auth(roles=["admin"])
@request_validator()
def edit_user(user_id):
    return jsonify(User.update(user_id, **request.json).self_dump()), 200


@api.route("/users/<int:user_id>", methods=["DELETE"])
@api_auth(roles=["admin"])
@request_validator()
def delete_user(user_id):
    return User.delete(user_id), 204
