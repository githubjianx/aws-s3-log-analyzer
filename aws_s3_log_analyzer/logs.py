import csv
import pandas as pd

from aws_s3_log_analyzer.files import read_path

def clean_log(log):
  ''' cleans log so it is valid csv '''
  # replace brackets with quotes
  return log.replace('[', '"', 1).replace(']', '"', 1)

def create_data_frame(logpath, fields):
  ''' returns dataframe containing interested fields + date from the logs '''
  df = pd.read_csv('./data/s3_log_field_list.txt', sep=' ', header=None)
  columns = df[1].tolist()
  csv_rows = s3_logs_to_csv_rows(logpath)
  df = pd.DataFrame.from_records(csv_rows, columns=columns)
  df['yyyy-mm-dd'] = pd.to_datetime(
                       df['timestamp'], format='%d/%b/%Y:%H:%M:%S +0000'
                     ).dt.date
  return df[fields + ['yyyy-mm-dd']]

def s3_logs_to_csv_rows(logpath):
  ''' converts s3 logs to csv format '''
  rows = []
  for log in read_path(logpath):
    csv_reader = csv.reader([clean_log(log)], delimiter=' ')
    # row is a list of fields in the log line
    for row in csv_reader:
      rows += [row]
  return rows
