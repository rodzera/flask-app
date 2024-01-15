from pytest import fixture

from src.app import application
from src.app.models import db


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
