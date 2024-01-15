from flask import abort
from typing import Literal
from sqlalchemy.orm.exc import DetachedInstanceError

from src.app.factory import db
from src.app.logger import get_logger

log = get_logger(__name__)


class BaseModel(object):
    """
    Base class for SQLAlchemy models.
    """

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        try:
            return f"<{self.__class__.__name__}> {self.id or '(draft)'}"
        except DetachedInstanceError:
            return f"<{self.__class__.__name__}> (detached)"

    def update_attrs(self, **kattrs):
        log.info(f"Updating model {self} attributes")

        for key, value in kattrs.items():
            if key == "password":
                raise AttributeError("Protected attribute")
            if hasattr(self, key):
                setattr(self, key, value)

        return self.orm("add")

    def orm(self, method: Literal["add", "delete"]):
        log.info(f"ORM operation '{method}' for model {self}")

        try:
            getattr(db.session, method)(self)
            db.session.commit()
        except Exception as e:
            log.exception(f"Exception while handling model {self}: {e}")
            db.session.rollback()
            abort(500)

        log.info("ORM handled successfully")
        return {} if method == "delete" else self

    @classmethod
    def get(cls, _id: int):
        return db.get_or_404(cls, _id, description=f"{cls.__name__} {_id} not found")

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def filter_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def w_entities(cls, *attrs, **kattrs):
        if not attrs:
            raise ValueError("Must provide model attrs")
        attrs = tuple(getattr(cls, attr) for attr in attrs)
        if not kattrs:
            return cls.query.with_entities(*attrs)
        return cls.query.with_entities(*attrs).filter_by(**kattrs)

    @classmethod
    def update(cls, _id: int, **kattrs):
        return cls.get(_id).update_attrs(**kattrs)

    @classmethod
    def delete(cls, _id: int):
        return cls.get(_id).orm("delete")
