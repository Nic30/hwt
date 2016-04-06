
SEPARATOR = '.'


class HdlRef():
    def __init__(self, names, caseSensitive, allChilds=False):
        if caseSensitive:
            self.names = tuple([n for n in names])
        else:
            self.names = tuple([n.lower() for n in names])
            
        self.all = allChilds

    @classmethod
    def fromJson(cls, jsn, caseSensitive):
        def flattern(jsn, op):
            try:
                binOp = jsn['binOperator']
            except KeyError:
                yield jsn['literal']
                raise StopIteration()
            if binOp['operator'] == op:
                yield from flattern(binOp['op0'], op)
                yield from flattern(binOp['op1'], op)
            else:
                yield binOp
        allChilds = False
        names = []
        # [TODO]
        for j in flattern(jsn, 'DOT'):
            t = j["type"]
            if t == 'ID':
                names.append(j['value'])
            elif t == "ALL":
                allChilds = True
            else:
                raise NotImplementedError("Not implemented for id part of type %s" % (t))
        return cls(names, caseSensitive, allChilds=allChilds)

    @classmethod
    def fromExprJson(cls, jExpr, caseSensitive):
        names = []
        v = jExpr['literal']
        assert(v["type"] == "ID")
        name = v['value']
        names.append(name)
        return cls(names, caseSensitive)

    # def __hash__(self):
    #    return hash(self.names)
    #
    # def __eq__(self, other):
    #    if len(self.names) == len(other.names):
    #        for s, o in zip(self.names, other.names):
    #            if s != o:
    #                return False
    #        return True
    #    return False
    #
    # def __ne__(self, other):
    #    return not self.__eq__(other)

    def __str__(self):
        s = SEPARATOR.join(self.names)
        if self.all:
            s += SEPARATOR + "all"
        return s

    def __repr__(self):
        return "<HdlRef  " + str(self) + ">"
