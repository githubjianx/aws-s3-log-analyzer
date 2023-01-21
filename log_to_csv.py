#!/usr/bin/env python

import argparse
import csv

from aws_s3_log_analyzer.logs import s3_logs_to_csv_rows

###########
# functions
###########

def parse_args():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )
  parser.add_argument(
    'logpath',
    help='''
    path to S3 logs, can be a file, example: ./data/sample_logs.txt,
    or a directory, example: ./data/sample_logs,
    in the case of a directory, all files in it will be read.
    '''
  )
  parser.add_argument(
    '--outfile',
    help='output file path',
    default='./logs.csv'
  )
  return parser.parse_args()

###########
# main code
###########

args = parse_args()
logpath, outfile = args.logpath, args.outfile

csv_rows = s3_logs_to_csv_rows(logpath)
with open(outfile, 'w', newline='') as outfile:
  writer = csv.writer(outfile, delimiter=',')
  for row in csv_rows:
    writer.writerow(row)
