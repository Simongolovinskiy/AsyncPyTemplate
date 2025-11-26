from enum import StrEnum
from typing import Literal


class LogLevel(StrEnum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogHandlerType(StrEnum):
    CONSOLE = "console"
    FILE = "file"
    LOKI = "loki"
    SENTRY = "sentry"
    GRAYLOG = "graylog"


LogOutput = Literal["stdout", "stderr"]