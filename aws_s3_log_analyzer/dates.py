from datetime import datetime
from pytz import UTC

def string_to_utc_date(str1):
  ''' convert a date string of format 1111-01-01 01:01:01 to a datetime object, utc assumed '''
  if isinstance(str1, str):
    date = datetime.strptime(str1, '%Y-%m-%d %H:%M:%S')
    return date.replace(tzinfo=UTC)
  else:
    return str1
