from summarize import *

def test_append_string_with_quotes():
  assert append_string_with_quotes('', 'bar') == '"bar" '
  assert append_string_with_quotes('foo ', 'bar') == 'foo "bar" '

def test_clean_log():
  log = '0e8b0fe19497f9f369651412f2300862af13c75e04427f61b8221c17c2f55dd0 foo-bucket [04/Jan/2023:23:35:33 +0000] 10.0.0.209 arn:aws:iam::12345:user/alice HRK5TQ4XK9KQPA06 REST.HEAD.OBJECT dir1/file1 "HEAD /dir1/file1 HTTP/1.1" 200 - - 5966 32 - "-" "Boto3/1.9.162 Python/3.8.2 Linux/4.19.0-17-cloud-amd64 Botocore/1.12.162" - aZP6Ng/0L1LOwWfP2tqDKbtE+rnXzAxvGDllW0a1sAuoGhkBWX3ZbYCInzWmC18ojwXr2NqjUkY= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader foo-bucket.s3.amazonaws.com TLSv1.2 - -'
  assert clean_log(log) == '0e8b0fe19497f9f369651412f2300862af13c75e04427f61b8221c17c2f55dd0 foo-bucket "04/Jan/2023:23:35:33 +0000" 10.0.0.209 alice HRK5TQ4XK9KQPA06 REST.HEAD.OBJECT dir1/file1 "HEAD /dir1/file1 HTTP/1.1" 200 - - 5966 32 - "-" "Boto3/1.9.162 Python/3.8.2 Linux/4.19.0-17-cloud-amd64 Botocore/1.12.162" - aZP6Ng/0L1LOwWfP2tqDKbtE+rnXzAxvGDllW0a1sAuoGhkBWX3ZbYCInzWmC18ojwXr2NqjUkY= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader foo-bucket.s3.amazonaws.com TLSv1.2 - -'

def test_construct_table_data_rows():
  summary = {
    'alice###/dir1/file1' : {
      '06/Feb/2019' : 10,
      '08/Feb/2019' : 5
    },
    'bob###/dir2/file2' : {
      '07/Feb/2019' : 3
    }
  }
  sorted_days = ['06/Feb/2019', '07/Feb/2019', '08/Feb/2019']
  assert construct_table_data_rows(summary, sorted_days, '###') == '"alice" "/dir1/file1" "10" "0" "5" \n"bob" "/dir2/file2" "0" "3" "0" \n'

def test_construct_table_header_row():
  interested_fields = [4, 7]
  sorted_days = ['06/Feb/2019', '07/Feb/2019', '08/Feb/2019']
  assert construct_table_header_row(interested_fields, sorted_days) == '"-" "-" "06/Feb/2019" "07/Feb/2019" "08/Feb/2019" '

def test_increment_dict_sub_key_count_empty_dict():
  dict1 = {}
  increment_dict_sub_key_count(dict1, 'foo', '123')
  assert dict1 == { 'foo': { '123': 1 } }
  dict1 = { 'foo': { '123': 1 } }
  increment_dict_sub_key_count(dict1, 'foo', '123')
  assert dict1 == { 'foo': { '123': 2 } }
  dict1 = { 'foo': { '123': 1 } }
  increment_dict_sub_key_count(dict1, 'bar', '123')
  assert dict1 == { 'foo': { '123': 1 }, 'bar': { '123': 1 } }

def test_skip_log():
  fields = ['abc', '123', 'def', '456', 'alice', 'ghi', '789']
  accounts = ['alice', 'bob']
  assert skip_log(fields, accounts) == False
  fields = 'abc 123 def 456 ecila ghi 789'
  assert skip_log(fields, accounts) == True
