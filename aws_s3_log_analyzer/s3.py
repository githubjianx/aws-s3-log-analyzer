import boto3
import os

from aws_s3_log_analyzer.files import make_dirs

def download(bucket, start_date, end_date, dest_dir):
  ''' download s3 bucket keys that were last modified within date range '''
  client = boto3.client('s3')
  [keys, keys_last_modified] = list_keys(client, bucket)
  wanted_keys = keys_last_modified_in_range(
                  keys, keys_last_modified, start_date, end_date
                )
  download_keys(client, bucket, wanted_keys, dest_dir)

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

def list_keys(client, bucket):
  ''' list all keys in s3 bucket '''
  keys = []
  keys_last_modified = []
  next_token = ''
  base_kwargs = {
    'Bucket':bucket
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
