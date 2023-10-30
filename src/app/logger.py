import logging
from os import path, mkdir


def set_logger_level(level: str):
    logger_level = logging._nameToLevel.get(level)
    for name in logging.root.manager.loggerDict:
        if name.startswith("src."):
            logger = logging.getLogger(name)
            logger.setLevel(logger_level)
            for h in logger.handlers:
                h.setLevel(logger_level)


def get_logger(name: str = None) -> logging.Logger:
    default_level = logging.DEBUG
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(funcName)s | %(lineno)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    sh = logging.StreamHandler()
    sh.setLevel(default_level)
    sh.setFormatter(formatter)

    if not path.exists("logs"):
        mkdir("logs")

    fh = logging.FileHandler("logs/app.log", mode="a")
    fh.setLevel(default_level)
    fh.setFormatter(formatter)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[fh, sh]
    )

    logger = logging.getLogger(name)
    logger.setLevel(default_level)
    return logger
