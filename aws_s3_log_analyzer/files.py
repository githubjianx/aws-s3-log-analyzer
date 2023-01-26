import errno
import glob
import os

from multiprocessing import Pool

def files(dirx):
  ''' globs all files in dir, recursively '''
  globstr = dirx + '/**'
  return [
    path for path in glob.glob(globstr, recursive=True)
    if os.path.isfile(path)
  ]

def make_dirs(paths):
  ''' creates the directories named in paths '''
  for path in paths:
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
      os.makedirs(dir_path)

def read_files_in_dir(dirx):
  ''' reads all files in dir, recursively '''
  lines_of_all_files = []
  with Pool(1) as pool:
    for lines_of_one_file in pool.map(read_path, files(dirx)):
      lines_of_all_files += lines_of_one_file
  return lines_of_all_files

def read_path(path):
  ''' reads path file or if it's a dir, all files in it '''
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
