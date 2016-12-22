from hwt.hdlObjects.hdlContext import HdlContext

class PackageHeader(HdlContext):
    """
    Hdl package container
    Entities means components from vhdl
    """
    def __init__(self, name, libraryCtx, isDummy=False):
        super(PackageHeader, self).__init__(name, libraryCtx)
        self.body = None
        self._isDummy = isDummy  
    
    def update(self, other):
        HdlContext.update(self, other)
        self.body = other.body
        
    def insertBody(self, body):
        self.body = body
        body.header = self
    
    def copyFrom(self, other):
        assert self._isDummy
        HdlContext.copyFrom(self, other)
        self._isDummy = False
        
class PackageBody(HdlContext):
    def __init__(self, name, libraryCtx):
        super(PackageBody, self).__init__(name, libraryCtx)
        self.header = None
