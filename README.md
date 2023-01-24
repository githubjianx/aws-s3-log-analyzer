# aws-s3-log-analyzer

A little command line script to help summarize [AWS S3 access logs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html) into a table.

Example usage:

Count unique requester/s3-key (see [field list](./data/s3_log_field_list.txt)) occurrences by day (on these [sample logs](./data/sample_logs.txt)):

```
$ ./summarize.py ./data/sample_logs.txt requester-id,s3-object-key
day                         06/Feb/2019  07/Feb/2019
requester-id s3-object-key                          
alice        '/bar.txt'               0            1
             '/foo.txt'               3            0
bob          '/foo.txt'               0            1
```

# requirements

- Python 3.9.10+

# setup

```
pip install -r requirements.txt
```

# testing

```
pytest
```

Or, run [pytest-watch](https://pypi.org/project/pytest-watch/) which runs Pytest whenever a test file is changed:

```
ptw
```

# run

```
./summarize.py --help
```
