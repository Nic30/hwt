
SEPARATOR = '.'

class VhdlLocalRef():
    def __init__(self, names):
        self.names = tuple([ n.lower() for n in names])
    @classmethod
    def fromJson(cls, jsn):
        names = list([j['value'].lower()  for j in jsn ])
        return cls(names)
    def __hash__(self):
        return hash(self.names)
        
    def __eq__(self, other):
        if len(self.names) == len(other.names):
            for s, o in zip(self.names, other.names):
                if s != o:
                    return False
            return True
        return False
    def __ne__(self, other):
        return not self.__eq__(other)
    def __str__(self):
        return SEPARATOR.join(self.names)
    def __repr__(self):
        return "<VhdlLocalRef  " + str(self) + ">"

class VhdlReference():
    def __init__(self, lib, localRef):
        self.lib = lib
        self.localRef = localRef
        self.name = lib + SEPARATOR + str(localRef)
    
    def __str__(self):
        return self.name
        
    @classmethod
    def fromJson(cls, jsn,):
        r = [ x['value'] for x in jsn]
        if jsn[-1]['type'] != "ID":
            r = [ x['value'] for x in jsn][:-1]  # cut last
            
        self = cls(r[0], VhdlLocalRef(r[1:]))
        return self


