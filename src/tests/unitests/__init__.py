from typing import Tuple
from base64 import b64encode
from unittest import TestCase as UnittestTestCase

from src.app.models import db
from src.app import application as app


class ProjectTest(UnittestTestCase):
    def setUp(self):
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        with self.ctx:
            db.create_all()

    def tearDown(self):
        self.ctx.pop()

    @staticmethod
    def create_app():
        return app

    @property
    def api_auth(self, cred: Tuple = ("admin", "admin")):
        u, p = cred
        credentials = f"{u}:{p}".encode()
        encoded_credentials = b64encode(credentials).decode()
        return {"Authorization": f"Basic {encoded_credentials}"}
