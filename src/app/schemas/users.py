from flask import current_app
from marshmallow import pre_load
from marshmallow.validate import ValidationError, Length

from src.app.schemas import ma
from src.app.logger import get_logger

log = get_logger(__name__)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        from src.app.models.users import User
        model = User
        load_instance = True

    model = Meta.model
    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(validate=Length(min=3, max=50))
    password = ma.auto_field(load_only=True, validate=Length(min=5, max=20))
    roles = ma.auto_field()

    @pre_load
    def validate_unique_username(self, data, **kwargs):
        if (username := data.get("username")) is None:
            return data

        if username == current_app.config["ADMIN_USER"]:
            raise ValidationError(message="Forbidden username", field_name="username")

        if self.model.w_entities("username", username=username).first():
            log.error(f"Username {username} is not unique")
            raise ValidationError(message="Username must be unique", field_name="username")
        return data

    @pre_load
    def validate_roles(self, data, **kwargs):
        if (roles := data.get("roles")) is None:
            return data

        from src.app.models.roles import Role
        [Role.get(role_id) for role_id in roles]
        return data
