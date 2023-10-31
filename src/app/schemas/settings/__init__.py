import logging
from marshmallow import post_load
from marshmallow.validate import OneOf

from src.app.schemas import ma
from src.app.logger import set_logger_level, get_logger

log = get_logger(__name__)


class LoggerLevelSchema(ma.Schema):
    level = ma.String(
        required=True,
        validate=OneOf(list(logging._nameToLevel.keys()))
    )

    @post_load
    def set_logger_level(self, data, **kwargs):
        level = data["level"]
        log.info(f"Setting logger level to: {level}")
        set_logger_level(level)
