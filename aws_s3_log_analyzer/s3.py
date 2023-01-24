import boto3
import os

def download(bucket, start_date, end_date, dest_dir):
  ''' downloads to dest dir those s3 bucket keys last modified in date range '''
  client = boto3.client('s3')
  [keys, keys_last_modified] = list_keys(client, bucket)
  wanted_keys = keys_last_modified_in_range(keys, keys_last_modified, start_date, end_date)
  download_keys(client, bucket, wanted_keys, dest_dir)

def download_keys(client, bucket, keys, dest_dir):
  ''' downloads s3 bucket keys to dest dir'''
  keys_and_paths = map_keys_to_paths(keys, dest_dir)
  paths = list(keys_and_paths.values())
  make_dirs(paths)
  download_keys_to_paths(client, bucket, keys_and_paths)

def download_keys_to_paths(client, bucket, keys_and_paths):
  ''' download s3 bucket keys to paths '''
  for k,p in keys_and_paths.items():
    client.download_file(bucket, k, p)

def keys_last_modified_in_range(keys, keys_last_modified, start_date, end_date):
  ''' returns s3 bucket keys that were last modified in date range '''
  return [
    k for idk, k in enumerate(keys)
    if keys_last_modified[idk] >= start_date and keys_last_modified[idk] <= end_date
  ]

def list_keys(client, bucket):
  ''' lists all keys in s3 bucket '''
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
      for i in contents:
        k = i.get('Key')
        keys.append(k)
        keys_last_modified.append(i.get('LastModified'))
    next_token = results.get('NextContinuationToken')
  return [keys, keys_last_modified]

def make_dirs(paths):
  ''' creates the directories named in paths '''
  for p in paths:
    dir_path = os.path.dirname(p)
    if not os.path.exists(dir_path):
      os.makedirs(dir_path)

def map_keys_to_paths(keys, dest_dir):
  ''' returns mapping of s3 bucket keys to their dest paths '''
  keys_and_paths = {}
  for k in keys:
    keys_and_paths[k] = os.path.join(dest_dir, k)
  return keys_and_paths
