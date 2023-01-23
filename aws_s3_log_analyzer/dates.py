from datetime import date as ddate, datetime
from pytz import UTC

def in_date_range(list1, list1_dates, start_date, end_date):
  '''
  each element in list1 is associated with a date in list1_dates,
  return the elements whose dates are within the date range of start_date to end_date
  '''
  agrees_with_start_date = [x for idx, x in enumerate(list1) if list1_dates[idx] >= start_date]
  agrees_with_end_date = [x for idx, x in enumerate(list1) if list1_dates[idx] <= end_date]
  return [x for x in agrees_with_start_date if x in agrees_with_end_date]

def string_to_utc_date(str1):
  ''' convert a date string of format 1111-01-01 01:01:01 to a datetime object, utc assumed '''
  if isinstance(str1, str):
    date = datetime.strptime(str1, '%Y-%m-%d %H:%M:%S')
    return date.replace(tzinfo=UTC)
  else:
    return str1
