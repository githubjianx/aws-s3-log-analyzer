#########
# imports
#########

import errno
import glob
import os

###########
# functions
###########

def files(dir1):
  ''' glob all files under dir, recursively '''
  globstr = dir1 + '/**'
  for file1 in glob.iglob(globstr, recursive=True):
    if os.path.isfile(file1):
      yield file1

def read_files_in_dir(dir1):
  ''' read all files in a directory, recursively '''
  lines = []
  for file1 in files(dir1):
    with open(file1, 'r') as reader:
      lines = lines + reader.readlines()
  return lines

def read_path(path):
  ''' read path file or if it's a directory, all the files in it '''
  lines = []
  if os.path.isfile(path):
    with open(path, 'r') as reader:
      lines = reader.readlines()
  elif os.path.isdir(path):
      lines = read_files_in_dir(path)
  else:
    raise FileNotFoundError(
      errno.ENOENT, os.strerror(errno.ENOENT), path 
    )
  return lines
