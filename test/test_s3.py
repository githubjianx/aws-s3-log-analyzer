from datetime import datetime, timedelta
from dateutil.tz import tzutc

import aws_s3_log_analyzer.s3

from aws_s3_log_analyzer.s3 import \
  keys_last_modified_in_range, \
  list_access_log_keys, \
  list_keys, \
  map_keys_to_paths

from test.fixtures.s3 import \
  expected_keys, \
  expected_keys_last_modified, \
  mock_list_prefix, \
  mock_s3_client

def describe_keys_last_modified_in_range():
  keys = ['foo', 'bar', 'baz']
  now = datetime.now()
  start_date = now - timedelta(days = 3)
  end_date = now - timedelta(days = 1)

  def all_in_range():
    keys_last_modified = [
      now - timedelta(days = 3),
      now - timedelta(days = 2),
      now - timedelta(days = 1)
    ]
    assert keys_last_modified_in_range(
            keys, keys_last_modified, start_date, end_date
           ) == keys

  def none_in_range():
    keys_last_modified = [
      now - timedelta(days = 5),
      now - timedelta(days = 4),
      now
    ]
    assert keys_last_modified_in_range(
            keys, keys_last_modified, start_date, end_date
           ) == []

  def some_in_range():
    keys_last_modified = [
      now - timedelta(days = 4),
      now - timedelta(days = 2),
      now
    ]
    assert keys_last_modified_in_range(
            keys, keys_last_modified, start_date, end_date
           ) == ['bar']

def describe_list_access_log_keys():
  def it_lists_keys_that_are_named_by_the_specified_days(mocker, mock_list_prefix):
    mocker.patch('aws_s3_log_analyzer.s3.list_keys').side_effect = mock_list_prefix
    spy = mocker.spy(aws_s3_log_analyzer.s3, "list_keys")
    keys, keys_last_modified = list_access_log_keys(
      None, 'foobucket', 'fooprefix/', ['2023-02-22', '2023-02-23']
    )
    assert spy.call_count == 2
    spy.assert_has_calls([
        mocker.call(None,'foobucket', 'fooprefix/2023-02-22-'),
        mocker.call(None,'foobucket', 'fooprefix/2023-02-23-')
    ])
    assert keys == [
      'fooprefix/2023-02-22-abc',
      'fooprefix/2023-02-23-abc'
    ]
    assert keys_last_modified == [
      datetime(2023, 1, 23, 1, 17, 7, tzinfo=tzutc()),
      datetime(2023, 1, 23, 1, 17, 7, tzinfo=tzutc())
    ]

def describe_list_keys():
  def it_lists_keys(expected_keys, expected_keys_last_modified, mock_s3_client):
    [keys, keys_last_modified] = list_keys(mock_s3_client, 'foobucket', 'fooprefix')
    assert keys == expected_keys
    assert keys_last_modified == expected_keys_last_modified

def describe_map_keys_to_paths():
  def no_keys():
    keys = []
    dest_dir = './logs'
    assert map_keys_to_paths(keys, dest_dir) == {}

  def one_key():
    keys = ['foo']
    dest_dir = './logs'
    assert map_keys_to_paths(keys, dest_dir) == {'foo': './logs/foo'}

  def two_keys():
    keys = ['foo', 'foo/bar']
    dest_dir = './logs'
    assert map_keys_to_paths(keys, dest_dir) == \
      {'foo': './logs/foo', 'foo/bar': './logs/foo/bar'}
