#!/usr/bin/env python

#########
# imports
#########

import argparse
import csv

###########
# functions
###########

def s3_logs_to_csv_rows(logfile):
  rows = []
  with open(logfile, 'r') as reader:
    log = reader.readline()
    while log != '':
      # replace brackets with quotes
      cleaned_log = log.replace('[', '"', 1).replace(']', '"', 1)
      csv_reader = csv.reader([cleaned_log], delimiter=' ')
      # row is a list of fields in the log line
      for row in csv_reader:
        # keep only the day in timestamp
        day = row[2].split(':')[0]
        row[2] = day

        rows += [row]
      log = reader.readline()
  return rows

###########
# main code
###########

def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("logfile", help=
    '''
    path to the S3 log file, example: /tmp/logs.txt
    ''')
  args = parser.parse_args()

  LOGFILE = args.logfile

  csv_rows = s3_logs_to_csv_rows(LOGFILE)
  output_file = LOGFILE + '.csv'
  with open(output_file, 'w', newline = '') as csv_file:
    writer = csv.writer(csv_file, delimiter = ',')
    for row in csv_rows:
      writer.writerow(row)

if __name__ == '__main__':
  main()
