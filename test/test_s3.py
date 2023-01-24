import os
import pytest

from datetime import datetime, timedelta

from aws_s3_log_analyzer.s3 import download, download_keys, list_keys, make_dirs, map_keys_to_paths, keys_last_modified_in_range
from test.fixtures.s3 import expected_keys, expected_keys_last_modified, mock_s3_client

def describe_download():
  pass

def describe_download_keys():
  pass

def describe_keys_last_modified_in_range():
  def all_in_range():
    keys = ['foo', 'bar']
    now = datetime.now()
    keys_last_modified = [
      now - timedelta(days = 1),
      now - timedelta(days = 2)
    ]
    start_date = now - timedelta(days = 3)
    end_date = now
    assert keys_last_modified_in_range(
            keys, keys_last_modified, start_date, end_date
           ) == keys

  def none_in_range():
    keys = ['foo', 'bar']
    now = datetime.now()
    keys_last_modified = [
      now - timedelta(days = 3),
      now
    ]
    start_date = now - timedelta(days = 2)
    end_date = now - timedelta(days = 1)
    assert keys_last_modified_in_range(
            keys, keys_last_modified, start_date, end_date
           ) == []

  def some_in_range():
    keys = ['foo', 'bar']
    now = datetime.now()
    keys_last_modified = [
      now - timedelta(hours = 36),
      now
    ]
    start_date = now - timedelta(days = 2)
    end_date = now - timedelta(days = 1)
    assert keys_last_modified_in_range(
            keys, keys_last_modified, start_date, end_date
           ) == ['foo']

def describe_list_keys():
  def gets_keys(expected_keys, expected_keys_last_modified, mock_s3_client):
    [keys, keys_last_modified] = list_keys(mock_s3_client, None)
    assert keys == expected_keys
    assert keys_last_modified == expected_keys_last_modified

def describe_make_dirs():
  def makes_nonexistent_dirs(mocker):
    mocker.patch('os.path.exists', return_value=False)
    mocker.patch('os.makedirs')
    os_makedirs_spy = mocker.spy(os, "makedirs")
    paths = ['foo/bar', 'bar/foo']
    make_dirs(paths)
    assert os_makedirs_spy.call_count == 2
    os_makedirs_spy.assert_has_calls([mocker.call('foo'), mocker.call('bar')])
  def skips_existent_dir(mocker):
    mocker.patch('os.path.exists').side_effect = [False, True]
    mocker.patch('os.makedirs')
    os_makedirs_spy = mocker.spy(os, "makedirs")
    paths = ['foo/bar', 'bar/foo']
    make_dirs(paths)
    assert os_makedirs_spy.call_count == 1
    os_makedirs_spy.assert_has_calls([mocker.call('foo')])

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
