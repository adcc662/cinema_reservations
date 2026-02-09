from datetime import datetime

import pytz


def get_time_zone():
    return "America/Mexico_City"


tz = pytz.timezone(get_time_zone())
