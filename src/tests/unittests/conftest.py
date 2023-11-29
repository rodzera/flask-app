from pytest import fixture

from src.app import application
from src.app.models import db
from src.app.models.roles import Role
from src.app.models.users import User


@fixture(autouse=True)
def ctx():
    ctx = application.app_context()
    with ctx:
        db.create_all()
        ctx.push()

    yield application

    with ctx:
        db.drop_all()
        ctx.pop()


@fixture()
def client(ctx):
    return ctx.test_client()


@fixture()
def runner(ctx):
    return ctx.test_cli_runner()


@fixture()
def populate_db():
    db.session.add_all(
        [
            User("admin", "admin", [Role("admin")]),
            User("user", "user", [Role("user")])
        ]
    )
    db.session.commit()
