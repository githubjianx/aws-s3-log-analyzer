import errno
import glob
import os

from multiprocessing import Pool

def files(dir1):
  ''' glob all files under dir, recursively '''
  globstr = dir1 + '/**'
  files = []
  for file1 in glob.glob(globstr, recursive=True):
    if os.path.isfile(file1):
      files += [file1]
  return files

def read_files_in_dir(dir1):
  ''' read all files in a directory, recursively '''
  lines_of_all_files = []
  with Pool(1) as pool:
    for lines_of_one_file in pool.map(read_path, files(dir1)):
      lines_of_all_files += lines_of_one_file
  return lines_of_all_files

def read_path(path):
  ''' read path file or if it's a directory, all the files in it '''
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
