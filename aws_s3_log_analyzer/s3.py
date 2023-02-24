import boto3
import os

from aws_s3_log_analyzer.dates import date_range_to_days_list
from aws_s3_log_analyzer.files import make_dirs

def download_access_logs(bucket, prefix, start_date, end_date, dest_dir):
  ''' download s3 access logs that were last modified within date range '''
  client = boto3.client('s3')
  # when access log files span years, listing them all take a long time.
  # since we have start and end dates, and that access log files have dates in their names.
  # we can be more specific about the listing, to speed it up.
  days = date_range_to_days_list(start_date, end_date)
  keys, keys_last_modified = list_access_log_keys(client, bucket, prefix, days)
  # still check against last modified
  filtered_keys = keys_last_modified_in_range(
    keys, keys_last_modified, start_date, end_date
  )
  download_keys(client, bucket, filtered_keys, dest_dir)

def download_keys(client, bucket, keys, dest_dir):
  ''' download s3 bucket keys '''
  keys_and_paths = map_keys_to_paths(keys, dest_dir)
  paths = list(keys_and_paths.values())
  make_dirs(paths)
  download_keys_to_paths(client, bucket, keys_and_paths)

def download_keys_to_paths(client, bucket, keys_and_paths):
  ''' download s3 bucket keys to specified paths '''
  for key, path in keys_and_paths.items():
    client.download_file(bucket, key, path)

def keys_last_modified_in_range(keys, keys_last_modified, start_date, end_date):
  ''' return list of s3 bucket keys that were last modified within date range '''
  return [
    key for index, key in enumerate(keys)
    if keys_last_modified[index] >= start_date and
      keys_last_modified[index] <= end_date
  ]

def list_access_log_keys(client, bucket, prefix, days):
  '''Return access log keys and their last modified time,
  for keys whose names start with any of the days specified.

  Access log key names start with the yyyy-mm-dd. For example:

  2023-02-22-00-15-29-D5DCE8A086530745

  If we are given:
  - prefix: foo/
  - days: 2023-02-21, 2023-02-22

  We list:
  - foo/2023-02-21-
  - foo/2023-02-22-
  '''
  keys = []
  keys_last_modified = []
  for day in days:
    full_prefix = prefix + day + '-'
    [day_keys, day_keys_last_modified] = list_keys(client, bucket, full_prefix)
    keys += day_keys
    keys_last_modified += day_keys_last_modified
  return keys, keys_last_modified

def list_keys(client, bucket, prefix):
  ''' list all keys in s3 bucket matching prefix '''
  keys = []
  keys_last_modified = []
  next_token = ''
  base_kwargs = {
    'Bucket':bucket,
    'Prefix':prefix
  }
  while next_token is not None:
    kwargs = base_kwargs.copy()
    if next_token != '':
      kwargs.update({'ContinuationToken': next_token})
    results = client.list_objects_v2(**kwargs)
    contents = results.get('Contents')
    if contents != None:
      for item in contents:
        key = item.get('Key')
        keys.append(key)
        keys_last_modified.append(item.get('LastModified'))
    next_token = results.get('NextContinuationToken')
  return [keys, keys_last_modified]

def map_keys_to_paths(keys, dest_dir):
  ''' return mapping of s3 bucket keys to their dest paths '''
  keys_and_paths = {}
  for key in keys:
    keys_and_paths[key] = os.path.join(dest_dir, key)
  return keys_and_paths
