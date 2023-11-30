from src.app.models import db
from src.app.models.base import BaseModel
from src.app.models.relationships import UsersRolesRelationship
from src.app.logger import get_logger

log = get_logger(__name__)


class Role(db.Model, BaseModel):
    __tablename__ = "roles"

    DEFAULT_ROLES = ("admin", "user")
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    users = db.relationship("User", secondary=UsersRolesRelationship, back_populates="roles")

    def __init__(self, name: str, users=None):
        if users is None:
            users = []

        self.name = name
        self.users = users


def create_default_roles():
    for role in Role.DEFAULT_ROLES:
        if Role.query.filter_by(name=role).first() is None:
            log.info(f"Creating role {role}")
            Role(name=role).orm_handler("add")
