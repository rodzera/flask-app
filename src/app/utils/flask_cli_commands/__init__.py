from flask import Flask

from src.app.models.roles import Role
from src.app.logger import get_logger

log = get_logger(__name__)


def register_cli_commands(app: Flask):
    @app.cli.command(name="populates_roles", help="Populates database with default roles.")
    def populates_roles():
        for role in ["admin", "user"]:
            if Role.query.filter_by(name=role).first() is None:
                log.info(f"Creating role {role}")
                Role(name=role).orm_handler("add")
