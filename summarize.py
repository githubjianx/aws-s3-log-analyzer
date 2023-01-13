#!/usr/bin/env python

#########
# imports
#########

import argparse
import csv
import re
import sys

##################
# helper functions
##################

def append_string_with_quotes(target_string, str1):
  ''' surround str1 with double quotes, then append to target_string, followed by a space '''
  append_string = '"%s" ' %str1
  return target_string + append_string

def clean_log(line):
  ''' clean up log '''
  # replace brackets with quotes
  new_line = line.replace('[', '"', 1).replace(']', '"', 1)
  # if requester is an AWS IAM user, the requester id will contain a long arn prefix, cut it out.
  new_line = re.sub(r"arn:aws:iam::\d+:user/", "", new_line)
  return new_line

def construct_table_data_rows(summary, sorted_days, delimiter):
  ''' construct data rows of the summary table '''
  # example:
  # foo    bar    ... 10   5    0    ...
  # oof    rab    ... 3    2    1    ...
  data_rows = ''
  for fields_string in sorted(summary.keys()):
    for field in fields_string.split(delimiter):
      data_rows = append_string_with_quotes(data_rows, field)
    for day in sorted_days:
      data_rows = append_string_with_quotes(data_rows, summary[fields_string].get(day, 0))
    data_rows += '\n'
  return data_rows

def construct_table_header_row(interested_fields, sorted_days):
  ''' construct header row of the summary table '''
  # example: field1 field2 ... day1 day2 day3 ...
  header_row = ''
  for field_num in interested_fields:
    # TODO: use field label ('requester', 'object-key', etc.) instead of '-'
    header_row = append_string_with_quotes(header_row, '-')
  for day in sorted_days:
    header_row = append_string_with_quotes(header_row, day)
  return header_row

def increment_dict_sub_key_count(dict1, key, sub_key):
  ''' increment sub_key's count by 1, take care if key does not exist '''
  dict1[key] = dict1.get(key, { sub_key: 0 })
  dict1[key][sub_key] = dict1[key].get(sub_key, 0) + 1

def skip_log(fields, requesters_to_skip):
  ''' decides whether a log should be skipped '''
  # skip if requester id matches any listed in requesters_to_skip
  # helpful if you are analyzing for security breach and want to ignore logs related to known good requesters
  return not any(element.lower() in fields[4].lower() for element in requesters_to_skip)

###########
# main code
###########

def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("logfile", help=
    '''
    path to the S3 log file, example: /tmp/logs.txt
    ''')
  parser.add_argument("field_numbers", help=
    '''
    comma delimited list of field numbers (starting from 0) in each S3 log to summarize
    for example, to summarize requester (field #4) and object key (field #7), specify: 4,7
    ''')
  args = parser.parse_args()

  LOGFILE = args.logfile

  # obtain an ordered list of integer field numbers
  interested_fields = sorted([int(numeric_string) for numeric_string in args.field_numbers.split(',')])

  # log summary is a count of unique values across all the interested fields, per day
  # for example, when interested fields are requester and object key:
  #
  # {
  #   'alice###/dir1/file1' : {
  #     '21/12/2022' : 10,
  #     '22/12/2022' : 5,
  #     ...
  #   },
  #   'bob###/dir2/file2' : {
  #     '22/12/2022' : 3,
  #     ...
  #   }
  #   ...
  # }
  #
  # there are 10 logs dated 21/12/2022 whose requester field = alice, key field = /dir1/file1
  # and so on
  #
  # notice the field values are concatenated with a delmiter so they can be split again when printing report
  summary = {}

  # keep track of unique days seen in logs
  days = set()

  # delimiter when concatenating field values, be sure the string never happens in the logs themselves
  DELIMIT = '###'

  requesters_to_skip = []

  # parse file, construct summary
  with open(LOGFILE, 'r') as reader:
    log = reader.readline()
    # parse log
    while log != '':
      skip = False
      csv_reader = csv.reader([clean_log(log)], delimiter=' ')
      # parse interested fields
      for fields in csv_reader:
        if skip_log(fields, requesters_to_skip):
          skip = True
          continue
        # track unique days seen
        ddmmyyyy = fields[2].split(':')[0]
        days.add(ddmmyyyy)
        # concatenate field values
        fields_string = '###'.join([fields[field_num] for field_num in interested_fields])
      if not skip:
        increment_dict_sub_key_count(summary, fields_string, ddmmyyyy)
      log = reader.readline()

  # print summary as a table
  sorted_days = sorted(days)
  print(construct_table_header_row(interested_fields, sorted_days))
  print(construct_table_data_rows(summary, sorted_days, DELIMIT))

if __name__ == '__main__':
  main()
