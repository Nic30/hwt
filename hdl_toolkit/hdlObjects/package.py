from hdl_toolkit.parser.hdlContext import HDLCtx

class PackageHeader(HDLCtx):
    """
    Entities means components from vhdl
    """
    def __init__(self, name, libraryCtx, isDummy=False):
        super(PackageHeader, self).__init__(name, libraryCtx)
        self.body = None
        self._isDummy = isDummy  
    
    def update(self, other):
        HDLCtx.update(self, other)
        self.body = other.body
        
    def insertBody(self, body):
        self.body = body
        body.header = self
    
    def copyFrom(self, other):
        assert self._isDummy
        HDLCtx.copyFrom(self, other)
        self._isDummy = False
        
class PackageBody(HDLCtx):
    def __init__(self, name, libraryCtx):
        super(PackageBody, self).__init__(name, libraryCtx)
        self.header = None
