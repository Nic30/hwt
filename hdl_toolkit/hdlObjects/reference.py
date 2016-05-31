
SEPARATOR = '.'


class HdlRef():
    def __init__(self, names, caseSensitive, allChilds=False):
        self.names = HdlRef._caseSensitivityForNames(caseSensitive, names)
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
            if t == 'ID' or t == "STRING":
                names.append(j['value'])
            elif t == "ALL":
                allChilds = True
            else:
                raise NotImplementedError("Not implemented for id part of type %s" % (t))
        return cls(names, caseSensitive, allChilds=allChilds)
    
    @staticmethod
    def _caseSensitivityForNames(caseSensitive, names):
        if caseSensitive:
            return names
        else:
            return tuple([n.lower() for n in names])

    @classmethod
    def fromExprJson(cls, jExpr, caseSensitive):
        names = []
        v = jExpr['literal']
        assert(v["type"] == "ID")
        name = v['value']
        names.append(name)
        names = HdlRef._caseSensitivityForNames(caseSensitive, names)
        return cls(names, caseSensitive)

    def __str__(self):
        s = SEPARATOR.join(self.names)
        if self.all:
            s += SEPARATOR + "all"
        return s

    def __repr__(self):
        return "<HdlRef  " + str(self) + ">"
