from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime


def get_time_zone():
    return "America/Mexico_City"


tz = pytz.timezone(get_time_zone())


def updated_at_column() -> Column:
    return Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz),
        nullable=False,
    )
