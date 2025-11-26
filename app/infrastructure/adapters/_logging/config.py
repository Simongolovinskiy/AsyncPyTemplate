import logging
from typing import Self, ClassVar
import msgspec
from loguru import logger

from app.domain.common.constants import SERVICE_NAME
from app.domain.common.enums import SecretsEnum
from app.domain.core.config.provider import SourceProviderPort

from .types import LogLevel
from .context import enrich


class BaseHandlerConfig(msgspec.Struct):
    enabled: bool = True
    level: LogLevel = LogLevel.INFO

    def apply(self) -> None:
        raise NotImplementedError


class ConsoleHandlerConfig(BaseHandlerConfig):
    colorful: bool = True
    output: str = "stderr"  # "stdout" | "stderr"

    def apply(self) -> None:
        sink = logging.sys.stderr if self.output == "stderr" else logging.sys.stdout
        fmt = (
            "<green>{time:HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<blue>req:{extra[request_id]}</blue> | "
            "<level>{message}</level>"
        )
        logger.add(
            sink,
            format=fmt if self.colorful else None,
            level=self.level,
            colorize=self.colorful,
            enqueue=True,
            serialize=not self.colorful,
        )


class FileHandlerConfig(BaseHandlerConfig):
    path: str = "logs/app.log"
    rotation: str = "10 MB"
    retention: str = "7 days"
    compression: str | None = "zip"

    def apply(self) -> None:
        logger.add(
            self.path,
            rotation=self.rotation,
            retention=self.retention,
            compression=self.compression,
            level=self.level,
            serialize=True,
            enqueue=True,
        )

class LokiHandlerConfig(BaseHandlerConfig):
    url: str = ""
    tags: dict[str, str] = msgspec.field(default_factory=dict)

    def apply(self) -> None:
        if not self.url:
            return

        try:
            from loguru_loki_handler import loki_handler  # ← правильный импорт!

            # Добавляем как sink (простой способ)
            logger.add(
                loki_handler(
                    url=self.url,
                    labels={"service_name": SERVICE_NAME, **self.tags}
                ),
                level=self.level,
                serialize=True,
                enqueue=True,
            )
            logger.info("Loki handler attached (loguru-loki-handler)", url=self.url)
        except ImportError:
            logger.warning("loguru-loki-handler not installed")
        except Exception as e:
            logger.warning(f"Loki handler failed: {e}")


class LoggerConfig(msgspec.Struct):
    level: LogLevel = LogLevel.INFO

    console: ConsoleHandlerConfig = msgspec.field(default_factory=ConsoleHandlerConfig)
    file: FileHandlerConfig = msgspec.field(default_factory=FileHandlerConfig)
    loki: LokiHandlerConfig = msgspec.field(default_factory=LokiHandlerConfig)

    _handlers: ClassVar[list[type[BaseHandlerConfig]]] = [
        ConsoleHandlerConfig,
        FileHandlerConfig,
        LokiHandlerConfig,
    ]

    @classmethod
    def load(cls, provider: SourceProviderPort) -> Self:
        return cls(
            level=provider.get_variable(SecretsEnum.LOG_LEVEL, LogLevel, default=LogLevel.INFO),
            console=ConsoleHandlerConfig(
                enabled=provider.get_variable(SecretsEnum.LOG_CONSOLE_ENABLED, bool, default=True),
                level=provider.get_variable(SecretsEnum.LOG_CONSOLE_LEVEL, LogLevel, default=LogLevel.INFO),
                colorful=provider.get_variable(SecretsEnum.LOG_CONSOLE_COLOR, bool, default=True),
                output=provider.get_variable(SecretsEnum.LOG_CONSOLE_OUTPUT, str, default="stderr"),
            ),
            file=FileHandlerConfig(
                enabled=provider.get_variable(SecretsEnum.LOG_FILE_ENABLED, bool, default=False),
                level=provider.get_variable(SecretsEnum.LOG_FILE_LEVEL, LogLevel, default=LogLevel.INFO),
                path=provider.get_variable(SecretsEnum.LOG_FILE_PATH, str, default="logs/app.log"),
            ),
            loki=LokiHandlerConfig(
                enabled=provider.get_variable(SecretsEnum.LOG_LOKI_ENABLED, bool, default=False),
                level=provider.get_variable(SecretsEnum.LOG_LOKI_LEVEL, LogLevel, default=LogLevel.INFO),
                url=provider.get_variable(SecretsEnum.LOG_LOKI_URL, str, default=""),
            ),
        )

    def setup(self) -> None:
        logger.remove()

        logger.configure(patcher=enrich)

        # Применяем все включённые хендлеры
        for attr_name in dir(self):
            config_obj = getattr(self, attr_name)
            if isinstance(config_obj, BaseHandlerConfig) and config_obj.enabled:
                config_obj.apply()

        # Перехват stdlib
        logging.getLogger().handlers = [InterceptHandler()]
        logging.getLogger().setLevel(logging.NOTSET)

        logger.info("Logging configured", level=self.level)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = logger.level(record.levelname).name
        depth = 6
        frame = logging.currentframe()
        while frame and any(x in frame.f_code.co_filename for x in ("logging", "loguru")):
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())