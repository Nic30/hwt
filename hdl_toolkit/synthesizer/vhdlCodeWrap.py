
class VhdlCodeWrap():
    def __init__(self, code_str):
        self.code_str = code_str
        
    def asVhdl(self, serializer, createTmpVarFn):
        return self.code_str
    
    def __str__(self):
        return self.asVhdl(None, None)