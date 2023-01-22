import pandas as pd
import pytest

@pytest.fixture
def sample_log_dir_files(sample_log_dir_path):
  file_names = ['xaa', 'xab', 'xac', 'xad', 'xae']
  return [sample_log_dir_path + '/' + filename for filename in file_names]

@pytest.fixture
def sample_log_dir_path():
  return './data/sample_logs'

@pytest.fixture
def sample_log_file_path():
  return './data/sample_logs.txt'

@pytest.fixture
def sample_logs_csv():
  return [
    ['79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be', 'DOC-EXAMPLE-BUCKET1', '06/Feb/2019:00:00:38 +0000', '192.0.2.3', 'alice', '3E57427F3EXAMPLE', 'REST.GET.VERSIONING', "'/foo.txt'", 'GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1', '200', '-', '1', '-', '7', '-', '-', 'S3Console/0.4', '-', 's9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234=', 'SigV4', 'ECDHE-RSA-AES128-GCM-SHA256', 'AuthHeader', 'DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com', 'TLSV1.2', 'arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP', 'Yes'],
    ['79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be', 'DOC-EXAMPLE-BUCKET1', '06/Feb/2019:00:00:38 +0000', '192.0.2.3', 'alice', '3E57427F3EXAMPLE', 'REST.GET.VERSIONING', "'/foo.txt'", 'GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1', '200', '-', '0', '-', '7', '-', '-', 'S3Console/0.4', '-', 's9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234=', 'SigV4', 'ECDHE-RSA-AES128-GCM-SHA256', 'AuthHeader', 'DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com', 'TLSV1.2', 'arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP', 'Yes'],
    ['79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be', 'DOC-EXAMPLE-BUCKET1', '06/Feb/2019:00:00:38 +0000', '192.0.2.3', 'alice', '3E57427F3EXAMPLE', 'REST.GET.VERSIONING', "'/foo.txt'", 'GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1', '200', '-', '0', '-', '7', '-', '-', 'S3Console/0.4', '-', 's9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234=', 'SigV4', 'ECDHE-RSA-AES128-GCM-SHA256', 'AuthHeader', 'DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com', 'TLSV1.2', 'arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP', 'Yes'],
    ['79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be', 'DOC-EXAMPLE-BUCKET1', '07/Feb/2019:00:00:38 +0000', '192.0.2.3', 'alice', '3E57427F3EXAMPLE', 'REST.GET.VERSIONING', "'/bar.txt'", 'GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1', '200', '-', '113', '-', '7', '-', '-', 'S3Console/0.4', '-', 's9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234=', 'SigV4', 'ECDHE-RSA-AES128-GCM-SHA256', 'AuthHeader', 'DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com', 'TLSV1.2', 'arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP', 'Yes'],
    ['79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be', 'DOC-EXAMPLE-BUCKET1', '07/Feb/2019:00:00:38 +0000', '192.0.2.3', 'bob', '3E57427F3EXAMPLE', 'REST.GET.VERSIONING', "'/foo.txt'", 'GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1', '200', '-', '113', '-', '7', '-', '-', 'S3Console/0.4', '-', 's9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234=', 'SigV4', 'ECDHE-RSA-AES128-GCM-SHA256', 'AuthHeader', 'DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com', 'TLSV1.2', 'arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP', 'Yes']
  ]

@pytest.fixture
def sample_logs_requester_object_day_df():
  columns = [
    "requester-id", "s3-object-key", "day"
  ]
  data = [
    ("alice", "'/foo.txt'", "06/Feb/2019"),
    ("alice", "'/foo.txt'", "06/Feb/2019"),
    ("alice", "'/foo.txt'", "06/Feb/2019"),
    ("alice", "'/bar.txt'", "07/Feb/2019"),
    ("bob", "'/foo.txt'", "07/Feb/2019")
  ]
  return pd.DataFrame.from_records(data, columns=columns)

@pytest.fixture
def sample_logs_txt():
  return [
    '''79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DOC-EXAMPLE-BUCKET1 [06/Feb/2019:00:00:38 +0000] 192.0.2.3 alice 3E57427F3EXAMPLE REST.GET.VERSIONING '/foo.txt' "GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1" 200 - 1 - 7 - "-" "S3Console/0.4" - s9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com TLSV1.2 arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP Yes\n''',
    '''79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DOC-EXAMPLE-BUCKET1 [06/Feb/2019:00:00:38 +0000] 192.0.2.3 alice 3E57427F3EXAMPLE REST.GET.VERSIONING '/foo.txt' "GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1" 200 - 0 - 7 - "-" "S3Console/0.4" - s9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com TLSV1.2 arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP Yes\n''',
    '''79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DOC-EXAMPLE-BUCKET1 [06/Feb/2019:00:00:38 +0000] 192.0.2.3 alice 3E57427F3EXAMPLE REST.GET.VERSIONING '/foo.txt' "GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1" 200 - 0 - 7 - "-" "S3Console/0.4" - s9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com TLSV1.2 arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP Yes\n''',
    '''79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DOC-EXAMPLE-BUCKET1 [07/Feb/2019:00:00:38 +0000] 192.0.2.3 alice 3E57427F3EXAMPLE REST.GET.VERSIONING '/bar.txt' "GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1" 200 - 113 - 7 - "-" "S3Console/0.4" - s9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com TLSV1.2 arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP Yes\n''',
    '''79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DOC-EXAMPLE-BUCKET1 [07/Feb/2019:00:00:38 +0000] 192.0.2.3 bob 3E57427F3EXAMPLE REST.GET.VERSIONING '/foo.txt' "GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1" 200 - 113 - 7 - "-" "S3Console/0.4" - s9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com TLSV1.2 arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP Yes\n'''
  ]
