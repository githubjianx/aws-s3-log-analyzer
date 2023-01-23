import boto3
import os

def download(bucket, start_date, end_date, dest_dir):
  keys = []
  keys_last_modified = []
  client = boto3.client('s3')

  list_keys(client, bucket, keys, keys_last_modified)

  wanted_keys = [
    x for idx, x in enumerate(keys)
    if keys_last_modified[idx] >= start_date and keys_last_modified[idx] <= end_date
  ]
  download_keys(client, bucket, wanted_keys, dest_dir)

def download_keys(client, bucket, keys, base_dir):
  ''' download keys from S3 bucket '''
  for k in keys:
    dest_pathname = os.path.join(base_dir, k)
    dir_path = os.path.dirname(dest_pathname)
    if not os.path.exists(dir_path):
      os.makedirs(dir_path)
    client.download_file(bucket, k, dest_pathname)

def list_keys(client, bucket, keys, keys_last_modified):
  ''' list all keys in S3 bucket '''
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
