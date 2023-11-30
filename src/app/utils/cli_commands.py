from flask import Flask

from src.app.models.roles import Role
from src.app.logger import get_logger

log = get_logger(__name__)

__all__ = ["register_cli_commands"]


def register_cli_commands(app: Flask):
    @app.cli.command(name="populate_roles", help="This function populates the database with default roles.")
    def populate_roles():
        for role in ["admin", "user"]:
            if Role.query.filter_by(name=role).first() is None:
                log.info(f"Creating role {role}")
                Role(name=role).orm_handler("add")
