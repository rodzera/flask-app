from werkzeug.security import generate_password_hash, check_password_hash

from src.app.models import db
from src.app.models.base import BaseModel
from src.app.models.relationships import UsersRolesRelationship


class User(db.Model, BaseModel):
    __tablename__ = "users"
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    roles = db.relationship("Role", secondary=UsersRolesRelationship, back_populates="users")

    def __init__(self, username: str, password: str, roles=None):
        if roles is None:
            roles = []

        self.username = username
        self.set_password(password)
        self.roles = roles
        self.orm("add")

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @staticmethod
    def schema():
        from src.app.schemas.users import UserSchema
        return UserSchema()
