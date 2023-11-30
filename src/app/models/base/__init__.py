from flask import abort
from typing import Literal
from sqlalchemy.orm.exc import DetachedInstanceError

from src.app.factory import db
from src.app.logger import get_logger

log = get_logger(__name__)


class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        try:
            return f"<{self.__class__.__name__}> {self.id or '(draft)'}"
        except DetachedInstanceError:
            return f"<{self.__class__.__name__}> (detached)"

    def update_attrs(self, **attrs):
        log.info(f"Updating attributes {attrs} for model {self}")
        for key, value in attrs.items():
            if key == "password":
                raise AttributeError("Protected attribute")
            if hasattr(self, key):
                setattr(self, key, value)
        return self.orm_handler("add")

    def orm_handler(self, method: Literal["add", "delete"]):
        log.debug(f"ORM operation '{method}' for model {self}")
        try:
            getattr(db.session, method)(self)
            db.session.commit()
            log.debug(f"ORM operation '{method}' completed successfully for model {self}")
            return self
        except Exception as e:
            log.exception(f"Exception handling model {self}: {e}")
            db.session.rollback()
            abort(500)
