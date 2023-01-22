import boto3
import os

from aws_s3_log_analyzer.dates import in_date_range

# adapted from: https://stackoverflow.com/questions/31918960/boto3-to-download-all-files-from-a-s3-bucket
def download(bucket, start_date, end_date, dest_dir):
  ''' copy the content of S3 bucket to local dir '''
  client = boto3.client('s3')
  keys = []
  keys_last_modified = []
  dirs = []
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
        if k[-1] != '/':
          keys.append(k)
          keys_last_modified.append(i.get('LastModified'))
        else:
          dirs.append(k)
    next_token = results.get('NextContinuationToken')

  keys = in_date_range(keys, keys_last_modified, start_date, end_date)

  for d in dirs:
    dest_pathname = os.path.join(dest_dir, d)
    if not os.path.exists(os.path.dirname(dest_pathname)):
      os.makedirs(os.path.dirname(dest_pathname))

  for k in keys:
    dest_pathname = os.path.join(dest_dir, k)
    if not os.path.exists(os.path.dirname(dest_pathname)):
      os.makedirs(os.path.dirname(dest_pathname))
    client.download_file(bucket, k, dest_pathname)
