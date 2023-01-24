import pytest

from datetime import datetime
from pytz import UTC

from aws_s3_log_analyzer.dates import string_to_utc_date

def describe_string_to_utc_date():
  def converts_string():
    str1 = '1990-01-01 01:01:01'
    date = datetime.strptime('1990-01-01 01:01:01', '%Y-%m-%d %H:%M:%S')
    date2 = date.replace(tzinfo=UTC)
    assert string_to_utc_date(str1) == date2

  def does_not_convert_datetime_object():
    date = datetime.now()
    assert string_to_utc_date(date) is date
