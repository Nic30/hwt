
class PackageHeader():
    def __init__(self, name):
        self.name = name
    
class Package(PackageHeader):
    def __init__(self, name, header):
        super(Package, self).__init__(name)
        self.header = header
    
    def insertBody(self, package):
        pass