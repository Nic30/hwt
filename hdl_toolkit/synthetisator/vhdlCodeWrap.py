
class VhdlCodeWrap():
    def __init__(self, code_str):
        self.code_str = code_str
        
    def asVhdl(self, serializer):
        return self.code_str
    
    def __str__(self):
        return self.asVhdl(None)
    
#class HdlFileReference():
#    def __init__(self, files):
#        self.files = files
#        
#    def asVhdl(self, serializer):
#        return "\n".join([serializer.comment(s) for s in self.files])
    