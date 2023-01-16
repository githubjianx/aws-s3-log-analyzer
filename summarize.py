#!/usr/bin/env python

#########
# imports
#########

import argparse
import openpyxl
import pandas as pd

from s3_log_to_csv import s3_logs_to_csv_rows

###########
# main code
###########

def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )
  parser.add_argument(
    'logpath',
    help='''
    path to S3 logs, can be a file, example: ./sample_logs.txt,
    or a directory, example: ./sample_logs,
    in the case of a directory, all files in it will be read recursively.
    '''
  )
  parser.add_argument(
    'fields',
    help='''
    list of fields in each S3 log to summarize, separated by comma,
    example: requester-id,s3-object-key'''
  )
  parser.add_argument('--excel-out', action='store_true', help='write summary to excel file')
  parser.add_argument('--excel-out-file', default='./summary.xlsx', help='excel output file path')
  args = parser.parse_args()

  LOGPATH = args.logpath
  fields = args.fields.split(',')
  excel_out = args.excel_out
  excel_out_file = args.excel_out_file

  # use dataframe to construct list of log field names
  df = pd.read_csv('s3_log_field_list.txt', sep=' ', header=None)
  columns = df[1].tolist()

  # create dataframe from logs csv data
  csv_rows = s3_logs_to_csv_rows(LOGPATH)
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

  excel_out and pivot.to_excel(excel_out_file)

if __name__ == '__main__':
  main()
