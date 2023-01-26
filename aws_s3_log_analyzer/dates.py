from datetime import datetime
from pytz import UTC

def string_to_utc_date(strx):
  ''' converts a date string of format 1990-01-01 01:01:01 to a datetime object, utc assumed '''
  if isinstance(strx, str):
    date = datetime.strptime(strx, '%Y-%m-%d %H:%M:%S')
    return date.replace(tzinfo=UTC)
  else:
    # not a string, do nothing
    return strx
