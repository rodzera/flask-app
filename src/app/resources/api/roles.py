from flask import request, jsonify

from src.app.logger import get_logger
from src.app.resources.api import api
from src.app.models.roles import Role
from src.app.utils import api_auth, request_validator


log = get_logger(__name__)


@api.route("/roles", methods=["GET"])
@api_auth(roles=["admin"])
@request_validator()
def get_roles():
    return jsonify({"roles": Role.dump_all()}), 200


@api.route("/roles/<int:role_id>", methods=["GET"])
@api_auth(roles=["admin"])
@request_validator()
def get_role(role_id):
    return jsonify(Role.dump(role_id)), 200


@api.route("/roles", methods=["POST"])
@api_auth(roles=["admin"])
@request_validator()
def post_role():
    return jsonify(Role.load(**request.json).self_dump()), 201


@api.route("/roles/<int:role_id>", methods=["PUT"])
@api_auth(roles=["admin"])
@request_validator()
def edit_role(role_id):
    return jsonify(Role.update(role_id, **request.json).self_dump()), 200


@api.route("/roles/<int:role_id>", methods=["DELETE"])
@api_auth(roles=["admin"])
@request_validator()
def delete_role(role_id):
    return Role.delete(role_id), 204
