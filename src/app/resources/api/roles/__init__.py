from flask import request, jsonify

from src.app.logger import get_logger
from src.app.utils import api_auth
from src.app.resources.api import api
from src.app.models import db
from src.app.models.roles import Role
from src.app.schemas.roles import RoleSchema
from src.app.utils.handlers.request import request_validator


log = get_logger(__name__)
schema = RoleSchema()


@api.route("/roles", methods=["GET"])
@api_auth(roles=["admin"])
@request_validator()
def get_roles():
    data = {"roles": [schema.dump(r) for r in Role.query.all()]}
    return jsonify(data), 200


@api.route("/roles/<int:role_id>", methods=["GET"])
@api_auth(roles=["admin"])
@request_validator()
def get_role(role_id):
    role = db.get_or_404(Role, role_id, "Role not found")
    return jsonify(schema.dump(role)), 200


@api.route("/roles", methods=["POST"])
@api_auth(roles=["admin"])
@request_validator()
def post_role():
    data = request.get_json()
    role = schema.load(data).orm_handler("add")
    return jsonify(schema.dump(role)), 201


@api.route("/roles/<int:role_id>", methods=["PUT"])
@api_auth(roles=["admin"])
@request_validator()
def edit_role(role_id):
    role = db.get_or_404(Role, role_id, "Role not found")
    data = request.get_json()
    schema.load(data)
    role = role.update_attrs(**data)
    return jsonify(schema.dump(role)), 200


@api.route("/roles/<int:role_id>", methods=["DELETE"])
@api_auth(roles=["admin"])
@request_validator()
def delete_role(role_id):
    role = db.get_or_404(Role, role_id, "Role not found")
    role.orm_handler("delete")
    return {}, 204
