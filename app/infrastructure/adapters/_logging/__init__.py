from __future__ import annotations

from loguru import logger
from loguru._logger import Logger
from app.domain.core.config.provider import SourceProviderPort, EnvSourceProvider

from .config import LoggerConfig

_INITIALIZED: bool = False


def get_logger(provider: SourceProviderPort = EnvSourceProvider()) -> Logger:
    global _INITIALIZED

    if _INITIALIZED:
        return logger

    config = LoggerConfig.load(provider)

    config.setup()

    _INITIALIZED = True

    logger.info(
        "Logger initialized successfully",
        level=config.level,
        handlers=[
            h.__class__.__name__
            for h in logger._core.handlers.values()
        ],
    )

    return logger