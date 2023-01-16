#!/usr/bin/env python

#########
# imports
#########

import argparse
import csv

from files import read_path

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
    path to S3 logs, can be a file, example: ./sample_logs.txt,
    or a directory, example: ./sample_logs,
    in the case of a directory, all files in it will be read.
    '''
  )
  parser.add_argument(
    '--outfile',
    help='output file path',
    default='./logs.csv'
  )
  return parser.parse_args()

def s3_logs_to_csv_rows(logpath):
  ''' convert s3 logs to csv format '''
  rows = []
  for log in read_path(logpath):
    # replace brackets with quotes
    cleaned_log = log.replace('[', '"', 1).replace(']', '"', 1)
    csv_reader = csv.reader([cleaned_log], delimiter=' ')
    # row is a list of fields in the log line
    for row in csv_reader:
      rows += [row]
  return rows

###########
# main code
###########

def main():
  args = parse_args()
  logpath = args.logpath
  outfile = args.outfile

  csv_rows = s3_logs_to_csv_rows(logpath)
  with open(outfile, 'w', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    for row in csv_rows:
      writer.writerow(row)

if __name__ == '__main__':
  main()
