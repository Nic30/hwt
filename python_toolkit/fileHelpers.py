
import os, fnmatch


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
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
    
    

    
    
