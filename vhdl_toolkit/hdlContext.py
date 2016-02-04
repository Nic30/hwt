from vhdl_toolkit.reference import VhdlRef 
from vhdl_toolkit.nonRedefDict import NonRedefDict
from vhdl_toolkit.types import VHDLType


class RequireImportErr(Exception):
    def __init__(self, reference):
        super(RequireImportErr, self).__init__()
        self.reference = reference
    
    def __str__(self):
        return "<RequireImportErr require to import %s first>" % (str(self.reference))
    
class HDLParseErr(Exception):
    pass

def mkType(name, width):
    t = VHDLType()
    t.name = name
    t.width = width
    return t


class BaseVhdlContext():
    integer = mkType("integer", int)
    positive = mkType("positive", int)
    natural = mkType("natural", int)
    boolean = mkType("boolean", bool)
    string = mkType("string", str)
    float = mkType("float", float)
   
    @classmethod 
    def importFakeIEEELib(cls, ctx):
        ctx.insert(FakeStd_logic_1164.std_logic_vector_ref, FakeStd_logic_1164.std_logic_vector)
        ctx.insert(FakeStd_logic_1164.std_logic_ref, FakeStd_logic_1164.std_logic)
        ctx.insert(VhdlRef(['ieee', 'std_logic_unsigned', 'CONV_INTEGER']), None)
        ctx.insert(VhdlRef(['ieee', 'std_logic_arith', 'IS_SIGNED']), None)
        ctx.insert(FakeStd_logic_1164.numeric_std_ref, FakeStd_logic_1164.numeric_std)
    
    @classmethod
    def getBaseCtx(cls):
        d = HDLCtx(None, None)
        for n in [cls.integer, cls.positive, cls.natural,
                   cls.boolean, cls.string, cls.float]:
            d[n.name] = n
        d['true'] = True
        d['false'] = False
        return d

class HDLCtx(NonRedefDict):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.entities = NonRedefDict()
        self.architectures = []
        self.packages = NonRedefDict()
        
    def importLibFromGlobal(self, ref):
        """
        Import for example lib.package to local context
        """
        top = self
        while top.parent is not None:
            top = top.parent
        try:
            toImport = top
            for n in ref.names:
                toImport = toImport[n]
            if ref.all:
                for n in toImport:
                    self[n] = toImport[n]
            else:
                raise NotImplementedError()
        except KeyError:
            raise RequireImportErr(ref)
    def lookupGlobal(self, ref):
        p = self
        n = ref.names[0] #[TODO]
        while p.parent is not None:
            p = p.parent
        if p is None:
            raise RequireImportErr(ref)
        try:
            for n in ref.names:
                p = p[n]
            return p
        except KeyError:
            raise RequireImportErr(ref)
        
    def lookupLocal(self, locRef):
        p = self
        n = locRef.names[-1] #[TODO]
        while p is not None:
            try:
                return p[n]
            except KeyError:
                p = p.parent
        
        raise Exception("Identificator %s not defined" % n)
    
    def insert(self, ref, val):
        c = self
        for n in ref.names[:-1]:
            c = c.setdefault(n, HDLCtx(n, c))
        c[ref.names[-1]] = val    
    def __str__(self):
        return "\n".join([
                    "\n".join([str(e) for _, e in self.entities.items()]),
                    "\n".join([str(a) for a in self.architectures]),
                    "\n".join([str(p) for p in self.packages]),
                    ])
class FakeStd_logic_1164():
    std_logic_vector = mkType("std_logic_vector", None)
    std_logic_vector_ref = VhdlRef(["ieee", "std_logic_1164", "std_logic_vector"])
    std_logic = mkType("std_logic", 1)
    std_logic_ref = VhdlRef(["ieee", "std_logic_1164", "std_logic"])
    numeric_std_ref = VhdlRef(["ieee", "numeric_std"])
    numeric_std = HDLCtx('numeric_std', None) 
        
