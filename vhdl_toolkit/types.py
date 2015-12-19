from ply.lex import LexToken

from vhdl_toolkit.parser_helpers import for_parentBlock

class INTF_DIRECTION():
    MASTER = "MASTER"
    SLEAVE = "SLEAVE"
    
    @classmethod
    def asDirection(cls, val):
        if val == INTF_DIRECTION.SLEAVE:
            return DIRECTION.IN 
        elif val == INTF_DIRECTION.MASTER:
            return DIRECTION.OUT
        else:
            raise Exception("Parameter is not interface direction")
    
    @classmethod
    def oposite(cls, d):
        if d == cls.SLEAVE:
            return cls.MASTER
        elif d == cls.MASTER:
            return cls.SLEAVE
        else:
            raise Exception("Parameter is not interface direction")
    

class DIRECTION():
    IN = "IN"
    OUT = "OUT"
    
    @classmethod
    def asIntfDirection(cls, d):
        if d == cls.IN:
            return INTF_DIRECTION.SLEAVE
        elif d == cls.OUT:
            return INTF_DIRECTION.MASTER
        else:
            raise Exception("Parameter is not direction")
    
    @classmethod
    def oposite(cls, d):
        if d == cls.IN:
            return cls.OUT
        elif d == cls.OUT:
            return cls.IN
        else:
            raise Exception("Parameter is not direction")
            


class VHDLType():
    """
    Vhdl type container
    """
    def __init__(self):
        self.str = None
    def parse(self, iterator):
        var_type = []   
        while True:
            tmp = next(iterator)
            if tmp.type == "RPAREN" or tmp.type == "ASSIG":
                iterator.__back__(tmp)
                break
            if tmp.type == "SEMICOLON":
                break
            if tmp.type == 'LPAREN':
                var_type.append(tmp)
                iterator.__back__(tmp)
                def add2type(iterator, o):
                    var_type.append(o)
                
                for_parentBlock(iterator, add2type)
                t = LexToken()
                t.type = 'RPAREN'
                t.value = ')'
                t.lineno = -1
                t.lexpos = -1
                var_type.append(t)
            else:    
                var_type.append(tmp)
        self.str = " ".join([ str(x.value) for x in var_type])
    def __str__(self):
        return self.str



class VHDLExtraType(object):
    """
    user type definition
    """
    @classmethod
    def createEnum(cls, name, values ):
        self = cls()
        self.name = name
        self.values = set(values)
        return self
            
    def __str__(self):
        return "TYPE %s IS (%s);" % (self.name, ", ".join(self.values) )

def STD_LOGIC():
    t = VHDLType()
    t.str = "std_logic"
    return t

def VHDLBoolean():
    return STD_LOGIC()
