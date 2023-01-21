import csv
import pandas as pd

from aws_s3_log_analyzer.files import read_path

def create_data_frame(logpath, fields):
  ''' create a data frame from log files '''
  # get a list of log field names, using a dataframe
  df = pd.read_csv('./data/s3_log_field_list.txt', sep=' ', header=None)
  columns = df[1].tolist()

  # create a logs dataframe
  csv_rows = s3_logs_to_csv_rows(logpath)
  df = pd.DataFrame.from_records(csv_rows, columns=columns)

  # add a column holding the day part of timestamp column
  df['day'] = df['timestamp'].str.split(':').str.get(0)

  # new dataframe with just the day column and the fields' columns
  return df[fields + ['day']]

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
