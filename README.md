# aws-s3-log-analyzer

A little command line script to help summarize [AWS S3 logs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html) into a table.

Example usage:

Count unique requester/s3-key (see [field list](./s3_log_field_list.txt)) occurrences by day (on these [sample logs](./sample_logs.txt)):

```
$ ./summarize.py sample_logs.txt requester-id,s3-object-key
timestamp                   06/Feb/2019  07/Feb/2019
requester-id s3-object-key
alice        '/bar.txt'               0            1
             '/foo.txt'               3            0
bob          '/foo.txt'               0            1
```

# Requirements

- Python 3.9.10+

# Setup

```
pip install -r requirements.txt
```

# Testing

```
pytest
```

# Run

```
./summarize.py --help
```

# Reference

- [Pandas API reference](https://pandas.pydata.org/docs/reference/index.html)

# Future Improvements

- Print all rows in pivot table output, and print full value of each cell
- `summarize.py` read S3 log field names from `s3_log_field_list.txt`
- Can work with multiple log files stored under a directory
- Pull log files from AWS by date range
- Convert tests to use pytest-describe
- Find a way to manage long lines (mostly string literals) in tests
