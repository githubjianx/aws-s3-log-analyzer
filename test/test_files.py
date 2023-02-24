import os

from aws_s3_log_analyzer.files import \
  files, \
  make_dirs, \
  read_files_in_dir, \
  read_path

from test.fixtures.sample_logs import \
  sample_log_dir_files, \
  sample_log_dir_path, \
  sample_log_file_path, \
  sample_logs_txt

def describe_files():
  def it_finds_them(sample_log_dir_path, sample_log_dir_files):
    assert sorted(files(sample_log_dir_path)) == sorted(sample_log_dir_files)

def describe_make_dirs():
  def it_makes_nonexistent_dirs(mocker):
    mocker.patch('os.path.exists', return_value=False)
    mocker.patch('os.makedirs')
    os_makedirs_spy = mocker.spy(os, "makedirs")
    paths = ['foo/bar', 'bar/foo']
    make_dirs(paths)
    assert os_makedirs_spy.call_count == 2
    os_makedirs_spy.assert_has_calls([mocker.call('foo'), mocker.call('bar')])
  def it_skips_existent_dir(mocker):
    mocker.patch('os.path.exists').side_effect = [False, True]
    mocker.patch('os.makedirs')
    os_makedirs_spy = mocker.spy(os, "makedirs")
    paths = ['foo/bar', 'bar/foo']
    make_dirs(paths)
    assert os_makedirs_spy.call_count == 1
    os_makedirs_spy.assert_has_calls([mocker.call('foo')])

def describe_read_files_in_dir():
  def it_reads_them(sample_log_dir_path, sample_logs_txt):
    assert sorted(read_files_in_dir(sample_log_dir_path)) == sorted(sample_logs_txt)

def describe_reads_path():
  def it_reads_file(sample_log_file_path, sample_logs_txt):
    assert read_path(sample_log_file_path) == sample_logs_txt
  def it_reads_dir(sample_log_dir_path, sample_logs_txt):
    assert sorted(read_path(sample_log_dir_path)) == sorted(sample_logs_txt)
