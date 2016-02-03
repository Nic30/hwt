
SEPARATOR = '.'

class VhdlRef():
    def __init__(self, names, allChilds=False):
        self.names = tuple([ n.lower() for n in names])
        self.all = allChilds
    @classmethod
    def fromJson(cls, jsn):
        allChilds = False
        names = []
        for j in jsn:
            t = j["type"]
            if t == 'ID':
                names.append(j['value'])
            elif t == "ALL":
                allChilds = True
        return cls(names, allChilds)
    #def __hash__(self):
    #    return hash(self.names)
    #    
    #def __eq__(self, other):
    #    if len(self.names) == len(other.names):
    #        for s, o in zip(self.names, other.names):
    #            if s != o:
    #                return False
    #        return True
    #    return False
    #
    #def __ne__(self, other):
    #    return not self.__eq__(other)
    
    def __str__(self):
        s = SEPARATOR.join(self.names)
        if self.all:
            s += SEPARATOR + "all"
        return s
    def __repr__(self):
        return "<VhdlRef  " + str(self) + ">"
