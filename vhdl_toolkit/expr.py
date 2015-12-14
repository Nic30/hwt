

def value2vhdlformat(dst, val):
    """ @param: dst is VHDLvariable connected with value """
    t = dst.var_type.str.lower()
    if hasattr(val, 'name') :
        return val.name
    if t == 'std_logic':
        return "'%d'" % (int(val))
    elif t.startswith("std_logic_vector"):
        return "STD_LOGIC_VECTOR(TO_UNSIGNED(%d, %s'LENGTH))" % (int(val), dst.name)
    else:
        raise Exception("value2vhdlformat can not resolve type conversion") 

class Map():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
   
    def __str__(self):
        return "%s => %s" %(self.dst.name, self.src.name)  
        
   
class Assignment():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        
    def __str__(self):
        return "%s <= %s"% (self.dst.name, value2vhdlformat(self.dst, self.src))
