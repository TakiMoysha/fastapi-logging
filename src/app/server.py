from contextlib import asynccontextmanager
from logging import getLogger
from fastapi import FastAPI
from app.config import get_config
from app.lib.utils.logging import get_logger_config

config = get_config()
logger = getLogger(__name__)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[%(asctime)s] %(levelprefix)s <%(name)s> %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # stderr
        },
    },
    "loggers": {
        "sqlalchemy.engine": get_logger_config(level=config.logging.sqlalchemy_level),
        "uvicorn.error": get_logger_config(level=config.logging.uvicorn_error_level),
        "uvicorn.access": get_logger_config(level=config.logging.uvicorn_access_level),
        "aiosqlite": get_logger_config(level=config.logging.not_interesting),
        "watchfiles.main": get_logger_config(level=config.logging.not_interesting),
        "httpx": get_logger_config(level=config.logging.not_interesting),
        "httpcore": get_logger_config(level=config.logging.not_interesting),
        "faker": get_logger_config(level=config.logging.not_interesting),
        "": get_logger_config(level=config.logging.app_level),
    },
}


def setup_logging(app: FastAPI):
    import logging.config

    logger.info("Plugin:Logging")
    logging.config.dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    logger.info(f"Lifespan:Server: <{str(config.server)}>")
    logger.info("Lifespan:Done: <>")
    yield
