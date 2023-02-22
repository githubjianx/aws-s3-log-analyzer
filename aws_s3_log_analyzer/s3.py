import boto3
import os

from aws_s3_log_analyzer.dates import date_range_to_days_list
from aws_s3_log_analyzer.files import make_dirs

def download_access_logs(bucket, prefix, start_date, end_date, dest_dir):
  ''' download s3 access logs that were last modified within date range '''
  client = boto3.client('s3')
  keys = list_access_log_keys(client, bucket, prefix, start_date, end_date)
  download_keys(client, bucket, keys, dest_dir)

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

def list_access_log_keys(client, bucket, prefix, start_date, end_date):
  '''return list of keys under the specified S3 bucket/prefix holding S3 access logs
  S3 creates a log file for every few access events.
  So there can be thousands and thousands of files/keys under the prefix.
  Listing them will take a long time.

  Since the keys are named after their dates, for example:
  2023-02-22-00-15-29-D5DCE8A086530745

  We make the prefix more specific, listing fewer keys, which is faster.

  For example, if we are given:
  - prefix: foo/
  - start_date: 2023-02-21...
  - end_date: 2023-02-22...

  We list only these prefixes:
  - foo/2023-02-21-
  - foo/2023-02-22-
  '''
  days = date_range_to_days_list(start_date, end_date)
  keys = []
  keys_last_modified = []
  for day in days:
    full_prefix = prefix + day + '-'
    [day_keys, day_keys_last_modified] = list_keys(client, bucket, full_prefix)
    keys += day_keys
    keys_last_modified += day_keys_last_modified
  # still check the keys' last modified date
  filtered_keys = keys_last_modified_in_range(
                  keys, keys_last_modified, start_date, end_date
                )
  return filtered_keys

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
