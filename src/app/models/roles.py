from src.app.models import db
from src.app.models.base import BaseModel
from src.app.models.schema import SchemaModel
from src.app.models.relationships import UsersRolesRelationship
from src.app.logger import get_logger

log = get_logger(__name__)


class Role(db.Model, BaseModel, SchemaModel):
    __tablename__ = "roles"
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    users = db.relationship("User", secondary=UsersRolesRelationship, back_populates="roles")
    
    DEFAULT_ROLES = ("admin", "user")

    def __init__(self, name: str, users=None):
        if users is None:
            users = []

        self.name = name
        self.users = users
        self.orm("add")

    @staticmethod
    def schema():
        from src.app.schemas.roles import RoleSchema
        return RoleSchema()

    @classmethod
    def create_default_roles(cls):
        for role in cls.DEFAULT_ROLES:
            if cls.w_entities("name", name=role).first() is None:
                log.info(f"Creating role {role}")
                cls(name=role)
