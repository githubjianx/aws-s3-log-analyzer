#!/usr/bin/env python

#########
# imports
#########

import argparse
import pandas as pd

from s3_log_to_csv import s3_logs_to_csv_rows

###########
# main code
###########

def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("logfile", help=
    '''
    path to the S3 log file, example: ./sample_logs.txt
    ''')
  parser.add_argument("fields", help=
    '''
    comma delimited list of fields in each S3 log to summarize
    for example, specify: requester-id,s3-object-key
    to summarize those fields
    ''')
  args = parser.parse_args()

  LOGFILE = args.logfile
  fields = args.fields.split(',')

  # initialize data frame
  csv_rows = s3_logs_to_csv_rows(LOGFILE)
  columns = ['bucket-owner-id', 'bucket-name', 'timestamp', 'ip-address', 'requester-id', 'request-id', 'operation', 's3-object-key', 'request-uri', 'http-status', 'error-code', 'bytes-sent', 'object-size', 'total-time', 'turn-around-time', 'referer', 'user-agent', 'version-id', 'host-id', 'signature-version', 'cipher', 'auth-type', 'host-header', 'tls-version', 'access-point-arn', 'acl-required']
  df = pd.DataFrame.from_records(csv_rows, columns=columns)

  # create a day column using the day part of timestamp column
  df['day'] = df['timestamp'].str.split(':').str.get(0)

  # cut out day column and those specified by fields arg
  df2 = df[fields + ['day']]

  pivot = df2.pivot_table(
    index=fields,
    columns='day',
    aggfunc=len,
    fill_value=0,
  )
  print(pivot)

if __name__ == '__main__':
  main()
