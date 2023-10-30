from flask import request, jsonify

from src.app.logger import get_logger
from src.app.utils import api_auth
from src.app.resources.api import api
from src.app.models.roles import Role
from src.app.schemas.roles import RoleSchema
from src.app.utils.handlers.request import request_validator


log = get_logger(__name__)
schema = RoleSchema()


@api.route("/roles", methods=["GET"])
@request_validator()
@api_auth(roles=["admin"])
def get_roles():
    data = {"roles": [schema.dump(r) for r in Role.query.all()]}
    return jsonify(data), 200


@api.route("/roles/<int:role_id>", methods=["GET"])
@request_validator()
@api_auth(roles=["admin"])
def get_role(role_id):
    role = Role.query.get_or_404(role_id, "Role not found")
    return jsonify(schema.dump(role)), 200


@api.route("/roles", methods=["POST"])
@request_validator(content_type=True)
@api_auth(roles=["admin"])
def post_role():
    data = request.get_json()
    role = schema.load(data).orm_handler("add")
    return jsonify(schema.dump(role)), 201


@api.route("/roles/<int:role_id>", methods=["PUT"])
@request_validator(content_type=True)
@api_auth(roles=["admin"])
def edit_role(role_id):
    role = Role.query.get_or_404(role_id, "Role not found")
    data = request.get_json()
    schema.load(data)
    role = role.update_attrs(**data)
    return jsonify(schema.dump(role)), 200


@api.route("/roles/<int:role_id>", methods=["DELETE"])
@request_validator()
@api_auth(roles=["admin"])
def delete_role(role_id):
    role = Role.query.get_or_404(role_id, "Role not found")
    role.orm_handler("delete")
    return {}, 204
