# aws_s3_log_analyzer

A little script to help summarize [AWS S3 logs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html).

Here's a sample log (see below for listing of its fields):

```
79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be DOC-EXAMPLE-BUCKET1 [06/Feb/2019:00:00:38 +0000] 192.0.2.3 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be 3E57427F3EXAMPLE REST.GET.VERSIONING - "GET /DOC-EXAMPLE-BUCKET1?versioning HTTP/1.1" 200 - 113 - 7 - "-" "S3Console/0.4" - s9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader DOC-EXAMPLE-BUCKET1.s3.us-west-1.amazonaws.com TLSV1.2 arn:aws:s3:us-west-1:123456789012:accesspoint/example-AP Yes
```

Suppose you have thousands of such logs covering multiple days, in a file called `logs.txt`, and you would like to count the unique requester/s3-key combinations per day, and have the output as a table, run:

```
./summarize.py logs.txt 4,7
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

# Fields in an S3 Log

```
field-num field-meaning

0 bucket owner id
1 bucket name
2 timestamp
3 IP address
4 requester id
5 request id
6 operation
7 s3 object key
8 request uri
9 http status
10 error code
11 bytes sent
12 object sizee
13 total time
14 turn around time
15 referer
16 user agent
17 version id
18 host id
19 signature version
20 cipher
21 auth type
22 host header
23 tls version
24 access point arrn
25 acl required
```

# Future Improvements

- Convert to use Panda and Pivot Table
- Convert tests to use pytest-describe
- Find a way to manage long lines (mostly string literals) in tests
