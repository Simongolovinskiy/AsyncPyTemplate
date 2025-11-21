from datetime import datetime

import pytz

TIMEZONE = "Europe/Moscow"


def get_current_datetime() -> datetime:
    timezone = pytz.timezone(TIMEZONE)
    return datetime.now(timezone)
