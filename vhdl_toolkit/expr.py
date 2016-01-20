

def value2vhdlformat(dst, val):
    """ @param: dst is VHDLvariable connected with value """
    if hasattr(val, 'name') :
        return val.name
    w = dst.var_type.getWidth()
    if w == 1:
        return "'%d'" % (int(val))
    elif w > 1:
        return "STD_LOGIC_VECTOR(TO_UNSIGNED(%d, %s'LENGTH))" % (int(val), dst.name)
    else:
        raise Exception("value2vhdlformat can not resolve type conversion") 

class Map():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
   
    def __str__(self):
        return "%s => %s" % (self.dst.name, self.src.name)  
        
   
class Assignment():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        
    def __str__(self):
        return "%s <= %s" % (self.dst.name, value2vhdlformat(self.dst, self.src))
