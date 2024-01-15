from unittest.mock import MagicMock

from src.app.models.schema import SchemaModel


def test_class_method_load(mocker):
    mocked_schema = mocker.patch.object(SchemaModel, "schema",  create=True)
    mocked_schema.return_value.load.return_value = []

    assert SchemaModel.load(test="test") == []
    mocked_schema.assert_called_once()
    mocked_schema.return_value.load.assert_called_once_with(test="test")


def test_class_method_dump(mocker):
    mocked_get = mocker.patch.object(SchemaModel, "get", create=True)
    mocked_schema = mocker.patch.object(SchemaModel, "schema",  create=True)
    mocked_schema.return_value.dump.return_value = []

    assert SchemaModel.dump(1) == []
    mocked_schema.assert_called_once()
    mocked_get.assert_called_once_with(1)
    mocked_schema.return_value.dump.assert_called_once_with(mocked_get.return_value)


def test_class_method_dump_all(mocker):
    mocked_method = mocker.patch.object(SchemaModel, "get_all", create=True)
    mock = MagicMock()
    mock.self_dump.return_value = "dumped"
    mocked_method.return_value = [mock]

    assert SchemaModel.dump_all() == [mock.self_dump.return_value]
    mocked_method.assert_called_once()
    mock.self_dump.assert_called_once()


def test_method_self_dump(mocker):
    mocked_schema = mocker.patch.object(SchemaModel, "schema",  create=True)
    mocked_schema.return_value.dump.return_value = []
    base = SchemaModel()

    assert base.self_dump() == []
    mocked_schema.assert_called_once()
    mocked_schema.return_value.dump.assert_called_once_with(base)
