from flask import request, jsonify

from src.app.logger import get_logger
from src.app.utils import api_auth
from src.app.resources.api import api
from src.app.models.users import User
from src.app.schemas.users import UserSchema
from src.app.utils.handlers.request import request_validator


log = get_logger(__name__)
schema = UserSchema()


@api.route("/users", methods=["GET"])
@request_validator()
@api_auth(roles=["admin"])
def get_users():
    data = {"users": [schema.dump(u) for u in User.query.all()]}
    return jsonify(data), 200


@api.route("/users/<int:user_id>", methods=["GET"])
@request_validator()
@api_auth(roles=["admin"])
def get_user(user_id):
    user = User.query.get_or_404(user_id, "User not found")
    return jsonify(schema.dump(user)), 200


@api.route("/users", methods=["POST"])
@request_validator(content_type=True)
@api_auth(roles=["admin"])
def post_user():
    data = request.get_json()
    user = schema.load(data).orm_handler("add")
    return jsonify(schema.dump(user)), 201


@api.route("/users/<int:user_id>", methods=["PUT"])
@request_validator(content_type=True)
@api_auth(roles=["admin"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id, "User not found")
    data = request.get_json()
    schema.load(data)
    user = user.update_attrs(**data)
    return jsonify(schema.dump(user)), 200


@api.route("/users/<int:user_id>", methods=["DELETE"])
@request_validator()
@api_auth(roles=["admin"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id, "User not found")
    user.orm_handler("delete")
    return {}, 204
