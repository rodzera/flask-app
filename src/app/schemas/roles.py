from marshmallow import pre_load
from marshmallow.validate import ValidationError, Length

from src.app.schemas import ma
from src.app.logger import get_logger

log = get_logger(__name__)


class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        from src.app.models.roles import Role
        model = Role
        load_instance = True

    model = Meta.model
    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(validate=Length(min=3, max=50))
    users = ma.auto_field()

    @pre_load
    def validate_unique_name(self, data, **kwargs):
        if (name := data.get("name")) is None:
            return data

        if self.model.w_entities("name", name=name).first():
            log.error(f"Name {name} is not unique")
            raise ValidationError(message="Name must be unique", field_name="name")
        return data

    @pre_load
    def validate_users(self, data, **kwargs):
        if (users := data.get("users")) is None:
            return data

        from src.app.models.users import User
        [User.get(user_id) for user_id in users]
        return data
