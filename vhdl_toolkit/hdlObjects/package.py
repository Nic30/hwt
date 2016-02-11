
class PackageHeader():
    def __init__(self, name):
        self.name = name
    
class PackageBody(PackageHeader):
    pass
    
class Package():
    def __init__(self, header, body):
        self.header = header
        self.body = body
        
    def getName(self):
        if self.header:
            return self.header.name
        else:
            return self.body.name