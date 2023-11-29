import logging
from pytest import raises
from marshmallow import ValidationError

from src.app.logger import get_logger
from src.app.schemas.settings import LoggerLevelSchema


def test_settings_schema_load():
    log = get_logger(__name__)
    LoggerLevelSchema().load({"level": "CRITICAL"})
    assert logging.getLevelName(log.level) == "CRITICAL"


def test_settings_schema_invalid_level():
    with raises(ValidationError) as exc:
        LoggerLevelSchema().load({"level": "LEVEL"})
    assert all([str(k) in str(exc.value) for k in logging._nameToLevel.keys()])
