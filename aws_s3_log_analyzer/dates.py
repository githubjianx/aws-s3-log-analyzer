from datetime import datetime, timedelta
from pytz import UTC

def date_range_to_days_list(start_date, end_date):
  '''return list of the days between start date and end date'''
  delta = end_date - start_date
  dates = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
  days = [date.strftime("%Y-%m-%d") for date in dates]
  return days

def string_to_utc_date(strx):
  ''' convert date string of format 1990-01-01 01:01:01 to a datetime object, utc assumed '''
  if isinstance(strx, str):
    date = datetime.strptime(strx, '%Y-%m-%d %H:%M:%S')
    return date.replace(tzinfo=UTC)
  else:
    # not a string, do nothing
    return strx
