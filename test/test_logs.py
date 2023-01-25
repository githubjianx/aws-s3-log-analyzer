import pandas as pd

from aws_s3_log_analyzer.logs import clean_log, create_data_frame, s3_logs_to_csv_rows
from test.fixtures.sample_logs import \
  sample_log_file_path, \
  sample_logs_csv, \
  sample_logs_requester_object_day_df, \
  sample_logs_txt, \
  sample_logs_txt_clean

def describe_clean_log():
  def cleans(sample_logs_txt, sample_logs_txt_clean):
    result = [clean_log(log) for log in sample_logs_txt]
    assert result == sample_logs_txt_clean

def describe_create_data_frame():
  def creates_requester_key_df(sample_log_file_path, sample_logs_requester_object_day_df):
    df = create_data_frame(sample_log_file_path, ['requester-id', 's3-object-key'])
    assert df.equals(sample_logs_requester_object_day_df)

def describe_s3_logs_to_csv_rows():
  def converts(sample_log_file_path, sample_logs_csv):
    assert s3_logs_to_csv_rows(sample_log_file_path) == sample_logs_csv
