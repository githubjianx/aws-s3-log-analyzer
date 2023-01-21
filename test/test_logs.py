from aws_s3_log_analyzer.logs import s3_logs_to_csv_rows

def test_s3_logs_to_csv_rows():
  ''' test rows returned by s3_logs_to_csv_rows match sample_logs.txt.csv '''
  logfile = './data/sample_logs.txt'
  logfile_csv = './data/sample_logs.txt.csv'

  rows = s3_logs_to_csv_rows(logfile)

  with open(logfile_csv, 'r') as reader:
    csv_lines = reader.read().splitlines()
  csv_lines_rows = [line.split(',') for line in csv_lines]

  assert rows == csv_lines_rows
