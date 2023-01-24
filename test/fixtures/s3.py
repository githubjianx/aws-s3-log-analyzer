import datetime
import pytest

from dateutil.tz import tzutc

@pytest.fixture
def expected_keys():
  return ['foo/sample_logs.txt', 'xaa', 'xab', 'xac', 'xad', 'xae']

@pytest.fixture
def expected_keys_last_modified():
  return [
    datetime.datetime(2023, 1, 23, 1, 17, 7, tzinfo=tzutc()),
    datetime.datetime(2023, 1, 23, 1, 5, 34, tzinfo=tzutc()),
    datetime.datetime(2023, 1, 23, 1, 5, 34, tzinfo=tzutc()),
    datetime.datetime(2023, 1, 23, 1, 5, 34, tzinfo=tzutc()),
    datetime.datetime(2023, 1, 23, 1, 5, 34, tzinfo=tzutc()),
    datetime.datetime(2023, 1, 23, 1, 5, 34, tzinfo=tzutc())
  ]

@pytest.fixture
def mock_s3_client():
  class mock_s3_client():
    def list_objects_v2(**kwargs):
      return {'ResponseMetadata': {'RequestId': '9RXQQ36V4AM0MYAE', 'HostId': 'K0jdVBSo2PnD9PYFCl71ewcFHoPXLu41nNmw+HyiCX1AABKs4T6Ea/gwCA2jfNKT5VqOo8DX2qo=', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'K0jdVBSo2PnD9PYFCl71ewcFHoPXLu41nNmw+HyiCX1AABKs4T6Ea/gwCA2jfNKT5VqOo8DX2qo=', 'x-amz-request-id': '9RXQQ36V4AM0MYAE', 'date': 'Mon, 23 Jan 2023 01:54:41 GMT', 'x-amz-bucket-region': 'us-east-1', 'content-type': 'application/xml', 'transfer-encoding': 'chunked', 'server': 'AmazonS3'}, 'RetryAttempts': 0}, 'IsTruncated': False, 'Contents': [{'Key': 'foo/sample_logs.txt', 'LastModified': datetime.datetime(2023, 1, 23, 1, 17, 7, tzinfo=tzutc()), 'ETag': '"6ff03d53ee2061a1b39f4d2154a5620c"', 'Size': 2497, 'StorageClass': 'STANDARD'}, {'Key': 'xaa', 'LastModified': datetime.datetime(2023, 1, 23, 1, 5, 34, tzinfo=tzutc()), 'ETag': '"1ac65e22e0812489f50ab345e0d83378"', 'Size': 499, 'StorageClass': 'STANDARD'}, {'Key': 'xab', 'LastModified': datetime.datetime(2023, 1, 23, 1, 5, 34, tzinfo=tzutc()), 'ETag': '"b8b7db176ddd0f575fd9427e2cfd57ba"', 'Size': 499, 'StorageClass': 'STANDARD'}, {'Key': 'xac', 'LastModified': datetime.datetime(2023, 1, 23, 1, 5, 34, tzinfo=tzutc()), 'ETag': '"b8b7db176ddd0f575fd9427e2cfd57ba"', 'Size': 499, 'StorageClass': 'STANDARD'}, {'Key': 'xad', 'LastModified': datetime.datetime(2023, 1, 23, 1, 5, 34, tzinfo=tzutc()), 'ETag': '"e45493a670cbef22e78a6424ccbba51a"', 'Size': 501, 'StorageClass': 'STANDARD'}, {'Key': 'xae', 'LastModified': datetime.datetime(2023, 1, 23, 1, 5, 34, tzinfo=tzutc()), 'ETag': '"166ad4943fd519eaefbc57f18fdf725e"', 'Size': 499, 'StorageClass': 'STANDARD'}], 'Name': 'jian-test-bucket', 'Prefix': '', 'MaxKeys': 1000, 'EncodingType': 'url', 'KeyCount': 6}
  return mock_s3_client
