from src.app.models import db
from src.app.models.base import BaseModel
from src.app.models.relationships import UsersRolesRelationship


class Role(db.Model, BaseModel):
    __tablename__ = "roles"

    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    users = db.relationship("User", secondary=UsersRolesRelationship, back_populates="roles")

    def __init__(self, name: str, users=None):
        if users is None:
            users = []

        self.name = name
        self.users = users
