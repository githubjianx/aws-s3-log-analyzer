from s3_log_to_csv import *

def test_s3_logs_to_csv_rows():
  ''' test rows returned by s3_logs_to_csv_rows match sample_logs.txt.csv '''
  logfile = './sample_logs.txt'
  logfile_csv = './sample_logs.txt.csv'

  rows = s3_logs_to_csv_rows(logfile)

  with open(logfile_csv, 'r') as reader:
    csv_lines = reader.read().splitlines()
  csv_lines_rows = [line.split(',') for line in csv_lines]

  assert rows == csv_lines_rows
