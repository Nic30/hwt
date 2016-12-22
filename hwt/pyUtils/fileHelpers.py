import os, fnmatch

def find_files(directory, pattern, recursive=True):
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
                yield filename
        
            
def applyReplacesOnFile(fileName, replaces, write=True):
    with open(fileName) as f:
        content = f.read()
    
    for r in replaces:
        content = content.replace(r, replaces[r])    
    if write:    
        with open(fileName, "w") as f:
            f.write(content)
    else:
        return content

class ChDir:
    """cd with backtrack"""         
    def __init__(self, newPath):  
        self.newPath = newPath
    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, type, value, tb):
        os.chdir(self.savedPath)