from flask import Flask

from src.app.models.roles import Role


__all__ = ["register_cli_commands"]


def register_cli_commands(app: Flask):
    @app.cli.command(name="populate_roles", help="This function populates the database with default roles.")
    def populate_roles():
        Role.create_default_roles()
