from vhdl_toolkit.hdlObjects.expr import value2vhdlformat

class Assignment():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        
    def __str__(self):
        return "%s <= %s" % (self.dst.name, value2vhdlformat(self.dst, self.src))
        #return "%s <= %s" % (self.dst.name, exp__str__(self.dst, self.src))
