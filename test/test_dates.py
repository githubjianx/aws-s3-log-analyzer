import pytest

from datetime import datetime
from pytz import UTC

from aws_s3_log_analyzer.dates import \
  date_range_to_days_list, \
  string_to_utc_date

def describe_date_range_to_days_list():
  def it_returns_the_in_range_days():
    start_date = datetime.strptime('1990-01-01 01:01:01', '%Y-%m-%d %H:%M:%S')
    start_date.replace(tzinfo=UTC)
    end_date = datetime.strptime('1990-01-03 01:01:01', '%Y-%m-%d %H:%M:%S')
    end_date.replace(tzinfo=UTC)
    assert date_range_to_days_list(start_date, end_date) == [
      '1990-01-01', '1990-01-02', '1990-01-03'
    ]

def describe_string_to_utc_date():
  def it_converts_string():
    strx = '1990-01-01 01:01:01'
    date = datetime.strptime('1990-01-01 01:01:01', '%Y-%m-%d %H:%M:%S')
    date2 = date.replace(tzinfo=UTC)
    assert string_to_utc_date(strx) == date2
  def it_does_not_convert_datetime_object():
    date = datetime.now()
    assert string_to_utc_date(date) is date
