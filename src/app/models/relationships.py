from src.app.models import db

UsersRolesRelationship = db.Table(
    "users_roles_relationship", db.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True)
)
