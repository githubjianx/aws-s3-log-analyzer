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

  # use dataframe to construct list of s3 log field names
  df = pd.read_csv('s3_log_field_list.txt', sep=' ', header=None)
  columns = df[1].tolist()

  # create dataframe from logs csv data
  csv_rows = s3_logs_to_csv_rows(LOGFILE)
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

  with pd.option_context(
    'display.max_rows', None,
    'display.width', None,
    'display.max_columns', None,
    ):
    print(pivot)

if __name__ == '__main__':
  main()
