"""
function to operate datetime objects
"""

import pytz

def convert_time_from_UTC(utc_dt):
    """converts given UTC time to Europe/Prague time

    Arguments:
        utc_dt {datetime} -- [in UTC]

    Returns:
        {datetime} -- [in Europe/Prague]
    """
    local_tz = pytz.timezone('Europe/Prague')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_dt