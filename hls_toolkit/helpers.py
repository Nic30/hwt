import os


class Chdir:
    """cd with backtrack"""         
    def __init__(self, newPath):  
        self.newPath = newPath
    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, type, value, tb):
        os.chdir(self.savedPath)