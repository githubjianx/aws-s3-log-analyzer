#!/usr/bin/env python

import argparse
import openpyxl
import pandas as pd

from aws_s3_log_analyzer.logs import create_data_frame

def parse_args():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )
  parser.add_argument(
    'logpath',
    help='''
    path to S3 logs, can be a file, example: ./data/sample_logs.txt,
    or a directory, example: ./sample_logs,
    in the case of a directory, all files in it will be read recursively.
    '''
  )
  parser.add_argument(
    'fields',
    help='''
    list of fields in each S3 log to summarize, separated by comma,
    example: requester-id,s3-object-key
    '''
  )
  parser.add_argument('--excel-out', action='store_true', help='write summary to excel file')
  parser.add_argument('--excel-out-file', default='./summary.xlsx', help='excel output file path')
  return parser.parse_args()

######
# main
######

args = parse_args()
logpath, fields, excel_out, excel_out_file = (
  args.logpath, args.fields.split(','), args.excel_out, args.excel_out_file
)

df = create_data_frame(logpath, fields)

# create and print summary

pivot = df.pivot_table(
  index=fields,
  columns='yyyy-mm-dd',
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
