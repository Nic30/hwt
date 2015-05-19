
from vhdl_toolkit.parser_helpers import for_parentBlock
from ply.lex import LexToken
from vhdl_toolkit.templates import VHDLTemplates 

class VHDLType():
    def __init__(self):
        self.str = None
    def parse(self, iterator):
        var_type = []   
        while True:
            tmp = next(iterator)
            if tmp.type == "RPAREN":
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
        self.str = " ".join([ x.value for x in var_type])
    def __str__(self):
        return self.str

class VHDLExtraType(object):
    @classmethod
    def createEnum(cls, name, values ):
        self = cls()
        self.name = name
        self.values = set(values)
        return self
            
    def __str__(self):
        return "TYPE %s IS (%s);" % (self.name, ", ".join(self.values) )
        
    
class PortItem(object):
    typeIn = "IN"
    typeOut = "OUT"
    def __init__(self, name, direction, var_type):
        self.name = name
        self.direction = direction
        self.var_type = var_type
    def __str__(self):
        return "%s : %s %s" % (self.name, self.direction, str(self.var_type))
        
class Entity(object):
    def __init__(self):
        self.port = []
        self.generics = []
        self.name = None
        
    def parse(self, tokens):
        tmp = next(tokens)
        if tmp.type != "ENTITY":
            raise Exception("Entity.parse expected ENTITY got %s" % tmp.type)
        tmp = next(tokens)  # id
        self.name = tmp.value
        tmp = next(tokens)  # is
        self._parse_port(tokens)
    def _parse_port(self, tokens):
        while next(tokens).type != "PORT": 
            pass
        def read_port_item(iterator, name):
            next(iterator)  # :
            direction = next(iterator)
            var_type = VHDLType()
            var_type.parse(iterator)
            p = PortItem(name.value, direction.type, var_type)
            self.port.append(p)    
            # print(name.value ,dd.value , direction.value, " ".join([ x.value for x in var_type] ))
        for_parentBlock(tokens, read_port_item)
    def __str__(self):
        return VHDLTemplates.entity.render(self.__dict__)