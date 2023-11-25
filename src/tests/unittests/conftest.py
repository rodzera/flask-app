import pytest

from src.app import application
from src.app.models import db
from src.app.models.roles import Role
from src.app.models.users import User


@pytest.fixture()
def app():
    with application.app_context():
        User.metadata.create_all(db.engine)
        Role.metadata.create_all(db.engine)
        db.session.add_all([
            User("admin", "admin", [Role("admin")]),
            User("user", "user", [Role("user")]),
        ])
        db.session.commit()

    yield application

    with application.app_context():
        db.session.remove()
        User.metadata.drop_all(db.engine)
        Role.metadata.drop_all(db.engine)


@pytest.fixture()
def client(app):
    return app.test_client()
