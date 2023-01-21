# aws_s3_log_analyzer

A little command line script to help summarize [AWS S3 logs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html) into a table.

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

# run

```
./summarize.py --help
```

# reference

- [Pandas API reference](https://pandas.pydata.org/docs/reference/index.html)

# future improvements

- pull log files from AWS by date range
- use Pandas to parse timestamp field as a datetime object
- convert tests to use pytest-describe
