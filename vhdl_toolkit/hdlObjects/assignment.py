class Assignment():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
   
    def __repr__(self):
        from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Assignment(self)    
