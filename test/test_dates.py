import pytest

from datetime import datetime, timedelta
from pytz import UTC

from aws_s3_log_analyzer.dates import in_date_range, string_to_utc_date

def describe_in_date_range():
  def gets_subset():
    list1 = ['foo', 'bar', 'baz', 'bing', 'bang']
    now = datetime.now()
    list1_dates = [
      now,
      now + timedelta(hours=12),
      now + timedelta(days=1),
      now + timedelta(hours=36),
      now + timedelta(days=2)
    ]
    start_date = now + timedelta(hours=12)
    end_date = now + timedelta(hours=36)
    assert in_date_range(list1, list1_dates, start_date, end_date) == \
      ['bar', 'baz', 'bing']

def describe_string_to_utc_date():
  def converts_string():
    str1 = '1990-01-01 01:01:01'
    date = datetime.strptime('1990-01-01 01:01:01', '%Y-%m-%d %H:%M:%S')
    date2 = date.replace(tzinfo=UTC)
    assert string_to_utc_date(str1) == date2

  def does_not_convert_datetime_object():
    date = datetime.now()
    assert string_to_utc_date(date) is date
