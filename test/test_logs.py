from aws_s3_log_analyzer.logs import create_data_frame, s3_logs_to_csv_rows
from test.fixtures.sample_logs import sample_log_file_path, sample_logs_csv, sample_logs_requester_object_day_df

def test_create_data_frame(
  sample_log_file_path,
  sample_logs_requester_object_day_df
):
  df = create_data_frame(sample_log_file_path, ['requester-id', 's3-object-key'])
  assert df.equals(sample_logs_requester_object_day_df)

def test_s3_logs_to_csv_rows(
  sample_log_file_path,
  sample_logs_csv
):
  assert s3_logs_to_csv_rows(sample_log_file_path) == sample_logs_csv
