#!/usr/bin/env python

#########
# imports
#########

import argparse
import csv
import errno
import glob
import os

###########
# functions
###########

def files(dir1):
  ''' glob all files under dir, recursively '''
  globstr = dir1 + '/**'
  for file1 in glob.iglob(globstr, recursive=True):
    if os.path.isfile(file1):
      yield file1

def read_logs(logpath):
  ''' read s3 logs stored at logpath '''
  logs = []
  if os.path.isfile(logpath):
    with open(logpath, 'r') as reader:
      logs = reader.readlines()
  elif os.path.isdir(logpath):
      logs = read_logs_from_dir(logpath)
  else:
    raise FileNotFoundError(
      errno.ENOENT, os.strerror(errno.ENOENT), logpath
    )
  return logs

def read_logs_from_dir(dir1):
  ''' read all s3 log files in a directory, recursively '''
  logs = []
  for file1 in files(dir1):
    with open(file1, 'r') as reader:
      logs = logs + reader.readlines()
  return logs

def s3_logs_to_csv_rows(logpath):
  ''' convert s3 logs to csv format '''
  rows = []
  for log in read_logs(logpath):
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

  args = parser.parse_args()

  LOGPATH = args.logpath
  outfile = args.outfile

  csv_rows = s3_logs_to_csv_rows(LOGPATH)
  with open(outfile, 'w', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    for row in csv_rows:
      writer.writerow(row)

if __name__ == '__main__':
  main()
