from aws_s3_log_analyzer.files import files, read_files_in_dir, read_path
from test.fixtures.sample_logs import sample_log_dir_files, sample_log_dir_path, sample_log_file_path, sample_logs_txt

def test_files(sample_log_dir_path, sample_log_dir_files):
  assert sorted(files(sample_log_dir_path)) == sorted(sample_log_dir_files)

def test_read_files_in_dir(sample_log_dir_path, sample_logs_txt):
  assert sorted(read_files_in_dir(sample_log_dir_path)) == sorted(sample_logs_txt)

def test_read_path_file(sample_log_file_path, sample_logs_txt):
  assert read_path(sample_log_file_path) == sample_logs_txt

def test_read_path_dir(sample_log_dir_path, sample_logs_txt):
  assert sorted(read_path(sample_log_dir_path)) == sorted(sample_logs_txt)
