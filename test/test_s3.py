from aws_s3_log_analyzer.s3 import download, download_keys, list_keys
from test.fixtures.s3 import expected_keys, expected_keys_last_modified, mock_s3_client

def describe_download():
  pass

def describe_download_keys():
  pass

def describe_list_keys():
  def gets_keys(expected_keys, expected_keys_last_modified, mock_s3_client):
    keys = []
    keys_last_modified = []
    list_keys(mock_s3_client, None, keys, keys_last_modified)
    assert keys == expected_keys
    assert keys_last_modified == expected_keys_last_modified
