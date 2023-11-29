from marshmallow import pre_load
from marshmallow.validate import ValidationError, Length

from src.app.models import db
from src.app.schemas import ma
from src.app.logger import get_logger
from src.app.models.users import User
from src.app.utils.helpers.queries import query_with_entities

log = get_logger(__name__)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(validate=Length(min=3, max=50))
    password = ma.auto_field(load_only=True, validate=Length(min=5, max=20))
    roles = ma.auto_field()

    @pre_load
    def validate_unique_username(self, data, **kwargs):
        if (username := data.get("username")) is None:
            return data

        if query_with_entities(User, "username", username=username).first():
            log.error(f"Username {username} is not unique")
            raise ValidationError(message="Username must be unique", field_name="username")
        return data

    @pre_load
    def validate_roles(self, data, **kwargs):
        if (roles := data.get("roles")) is None:
            return data

        from src.app.models.roles import Role
        [db.get_or_404(Role, role_id, description=f"Role {role_id} not found") for role_id in roles]
        return data
