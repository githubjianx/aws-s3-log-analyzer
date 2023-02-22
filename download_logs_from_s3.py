#!/usr/bin/env python

import argparse

from datetime import date as ddate, datetime, timedelta
from pytz import UTC

from aws_s3_log_analyzer.dates import string_to_utc_date
from aws_s3_log_analyzer.s3 import download

def parse_args():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )
  parser.add_argument(
    's3_bucket',
    help='''
    name of the S3 bucket that holds access logs (of other S3 buckets),
    example: my-test-bucket
    '''
  )
  parser.add_argument(
    '--prefix',
    default='/',
    help='''
    only look at log files under this prefix.
    '''
  )
  parser.add_argument(
    '--start_date',
    default=datetime.now(tz=UTC) - timedelta(days=1),
    help='''
    download only log files last modified on this date (utc) or after,
    example: '2023-01-22 20:00:00'
    '''
  )
  parser.add_argument(
    '--end_date',
    default=datetime.now(tz=UTC),
    help='''
    download only log files last modified on this date (utc) or before,
    example: '2023-01-22 20:00:00'
    '''
  )
  parser.add_argument(
    '--dest_base_dir',
    default='./logs',
    help='''
    base directory for downloaded files,
    files from foo-bucket will be downloaded into a sub-directory within the base directory,
    for example, if base directory is './logs',
    files will be downloaded to './logs/foo-bucket'.
    '''
  )
  return parser.parse_args()

######
# main
######

args = parse_args()
s3_bucket, prefix, start_date, end_date, dest_base_dir  = (
  args.s3_bucket, args.prefix, args.start_date, args.end_date, args.dest_base_dir
)

start_date_obj = string_to_utc_date(start_date)
end_date_obj = string_to_utc_date(end_date)
if start_date_obj > end_date_obj:
  raise ValueError('start_date is after end_date')

dest_dir = dest_base_dir + '/' + s3_bucket

download(s3_bucket, prefix, start_date_obj, end_date_obj, dest_dir)
