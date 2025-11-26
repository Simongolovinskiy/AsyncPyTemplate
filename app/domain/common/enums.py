from enum import StrEnum, auto


class UpperStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name.upper()


class CacheKey(StrEnum):
    PRODUCT = "product:"


# env names, example: os.getenv(SecretsEnum.DATABASE_CONNECTION_STRING)
class SecretsEnum(UpperStrEnum):
    # Common
    DATABASE_CONNECTION_STRING = auto()
    CACHE_HOST = auto()
    CACHE_PORT = auto()
    CACHE_DB = auto()
    CACHE_PASSWORD = auto()
    CACHE_SSL = auto()
    CACHE_DECODE_RESPONSES = auto()
    KAFKA_BOOTSTRAP_SERVERS = auto()
    KAFKA_GROUP_ID = auto()

    # Logging
    LOG_LEVEL = auto()
    LOG_CONSOLE_ENABLED = auto()
    LOG_CONSOLE_LEVEL = auto()
    LOG_CONSOLE_COLOR = auto()
    LOG_CONSOLE_OUTPUT = auto()
    LOG_FILE_ENABLED = auto()
    LOG_FILE_LEVEL = auto()
    LOG_FILE_PATH = auto()
    LOG_LOKI_ENABLED = auto()
    LOG_LOKI_LEVEL = auto()
    LOG_LOKI_URL = auto()
    LOG_SENTRY_ENABLED = auto()
    LOG_SENTRY_LEVEL = auto()
    LOG_SENTRY_DSN = auto()
    LOG_GRAYLOG_ENABLED = auto()
    LOG_GRAYLOG_LEVEL = auto()
    LOG_GRAYLOG_HOST = auto()
    LOG_GRAYLOG_PORT = auto()
