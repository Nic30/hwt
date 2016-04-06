
class VhdlCodeWrap():
    def __init__(self, code_str):
        self.code_str = code_str
        
    def asVhdl(self, serializer):
        return self.code_str
        
