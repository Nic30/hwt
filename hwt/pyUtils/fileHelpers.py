import fnmatch
import os


def find_files(directory, pattern, recursive=True):
    """
    Find files by pattern in directory
    """
    if not os.path.isdir(directory):
        if os.path.exists(directory):
            raise IOError(directory + ' is not directory')
        else:
            raise IOError(directory + " does not exists")
    if recursive:
        for root, _, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    yield filename
    else:
        root = directory
        for basename in os.listdir(root):
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                if os.path.isfile(filename):
                    yield filename
