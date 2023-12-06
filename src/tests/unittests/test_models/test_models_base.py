from pytest import raises
from unittest.mock import PropertyMock, MagicMock
from werkzeug.exceptions import InternalServerError
from sqlalchemy.orm.exc import DetachedInstanceError

from src.app.models.base import BaseModel


def test_attributes():
    assert hasattr(BaseModel, "id")
    assert hasattr(BaseModel, "created_at")
    assert hasattr(BaseModel, "updated_on")


def test_method_repr(mocker):
    mocker.patch.object(BaseModel, "id")
    base = BaseModel()
    base.id = 666
    assert base.__repr__() == f"<BaseModel> {666}"


def test_method_repr_detached_instance_error(mocker):
    mocker.patch.object(BaseModel, "id")
    base = BaseModel()
    type(base).id = PropertyMock(side_effect=DetachedInstanceError)
    assert base.__repr__() == f"<BaseModel> (detached)"


def test_method_orm_add(mocker):
    mocked_db = mocker.patch("src.app.models.base.db")
    mocker.patch.object(BaseModel, "__str__").return_value = "MagicMock"

    base = BaseModel()
    assert base == base.orm("add")
    mocked_db.session.add.assert_called_once_with(base)
    mocked_db.session.commit.assert_called_once_with()


def test_method_orm_delete(mocker):
    mocked_db = mocker.patch("src.app.models.base.db")
    mocker.patch.object(BaseModel, "__str__").return_value = "MagicMock"

    base = BaseModel()
    assert {} == base.orm("delete")
    mocked_db.session.delete.assert_called_once_with(base)
    mocked_db.session.commit.assert_called_once_with()


def test_method_orm_rollback(mocker):
    mocked_db = mocker.patch("src.app.models.base.db")
    mocked_db.session.commit.side_effect = Exception
    mocker.patch.object(BaseModel, "__str__").return_value = "MagicMock"

    with raises(InternalServerError) as exc:
        BaseModel().orm("add")
    mocked_db.session.rollback.assert_called_once()
    assert InternalServerError.description in str(exc.value)


def test_method_update_attrs(mocker):
    mocker.patch.object(BaseModel, "__str__").return_value = "MagicMock"
    mocked_method = mocker.patch.object(BaseModel, "orm")

    base = BaseModel()
    mocked_method.return_value = base

    assert base == base.update_attrs(id=1, created_at=2, updated_on=3)
    assert base.id == 1
    assert base.created_at == 2
    assert base.updated_on == 3
    mocked_method.assert_called_once_with("add")


def test_method_update_attrs_attribute_error(mocker):
    mocker.patch.object(BaseModel, "__str__").return_value = "MagicMock"

    with raises(AttributeError) as exc:
        BaseModel().update_attrs(password="password")
    assert "Protected attribute" in str(exc.value)


def test_class_method_get(mocker):
    mocked_db = mocker.patch("src.app.models.base.db")
    mocked_db.get_or_404.return_value = []

    assert BaseModel.get(1) == []
    mocked_db.get_or_404.assert_called_once_with(BaseModel, 1, description="BaseModel 1 not found")


def test_class_method_get_all(mocker):
    mocked_method = mocker.patch.object(BaseModel, "query")
    mocked_method.all.return_value = []

    assert BaseModel.get_all() == []
    mocked_method.all.assert_called_once()


def test_class_method_filter_by(mocker):
    mocked_method = mocker.patch.object(BaseModel, "query")
    mocked_method.filter_by.return_value = []

    assert BaseModel.filter_by() == []
    mocked_method.filter_by.assert_called_once()


def test_class_method_w_entities_value_error():
    with raises(ValueError) as exc:
        BaseModel.w_entities()
    assert "Must provide model attrs" in str(exc.value)


def test_class_method_w_entities_with_attrs(mocker):
    mocked_method = mocker.patch.object(BaseModel, "query")

    BaseModel.w_entities("id", "created_at", "updated_on")
    mocked_method.with_entities.assert_called_once_with(BaseModel.id, BaseModel.created_at, BaseModel.updated_on)
    mocked_method.with_entities.return_value.filter_by.assert_not_called()


def test_class_method_w_entities_with_kattrs(mocker):
    mocked_method = mocker.patch.object(BaseModel, "query")

    BaseModel.w_entities("id", "created_at", "updated_on", id=1, created_at=2, updated_on=3)
    mocked_method.with_entities.assert_called_once_with(BaseModel.id, BaseModel.created_at, BaseModel.updated_on)
    mocked_method.with_entities.return_value.filter_by.assert_called_once_with(id=1, created_at=2, updated_on=3)


def test_class_method_load(mocker):
    mocked_schema = mocker.patch.object(BaseModel, "schema")
    mocked_schema.return_value.load.return_value = []

    assert BaseModel.load(test="test") == []
    mocked_schema.assert_called_once()
    mocked_schema.return_value.load.assert_called_once_with(test="test")


def test_class_method_update(mocker):
    mocked_method = mocker.patch.object(BaseModel, "get")
    mocked_method.return_value.update_attrs.return_value = []

    assert BaseModel.update(1, test="test") == []
    mocked_method.assert_called_once_with(1)
    mocked_method.return_value.update_attrs.assert_called_once_with(test="test")


def test_class_method_delete(mocker):
    mocked_method = mocker.patch.object(BaseModel, "get")
    mocked_method.return_value.orm.return_value = []

    assert BaseModel.delete(1) == []
    mocked_method.assert_called_once_with(1)
    mocked_method.return_value.orm.assert_called_once_with("delete")


def test_class_method_dump(mocker):
    mocked_get = mocker.patch.object(BaseModel, "get")
    mocked_schema = mocker.patch.object(BaseModel, "schema")
    mocked_schema.return_value.dump.return_value = []

    assert BaseModel.dump(1) == []
    mocked_schema.assert_called_once()
    mocked_get.assert_called_once_with(1)
    mocked_schema.return_value.dump.assert_called_once_with(mocked_get.return_value)


def test_class_method_dump_all(mocker):
    mocked_method = mocker.patch.object(BaseModel, "get_all")
    mock = MagicMock()
    mock.self_dump.return_value = "dumped"
    mocked_method.return_value = [mock]

    assert BaseModel.dump_all() == [mock.self_dump.return_value]
    mocked_method.assert_called_once()
    mock.self_dump.assert_called_once()


def test_method_self_dump(mocker):
    mocked_schema = mocker.patch.object(BaseModel, "schema")
    mocked_schema.return_value.dump.return_value = []
    base = BaseModel()

    assert base.self_dump() == []
    mocked_schema.assert_called_once()
    mocked_schema.return_value.dump.assert_called_once_with(base)
