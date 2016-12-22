from hwt.pyUtils.nonRedefDict import NonRedefDict
from hwt.hdlObjects.reference import HdlRef
from hwt.hdlObjects.entity import Entity
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdlObjects.architecture import Architecture
from hwt.hdlObjects.function import Function
from hwt.hdlObjects.functionContainer import FunctionContainer

class RequireImportErr(Exception):
    """Is raised when program can not approach without importing specific reference"""
    def __init__(self, reference):
        super(RequireImportErr, self).__init__()
        self.reference = reference
        self.fileName = None
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        if self.fileName:
            fileName = 'file %s' % self.fileName
        else:
            fileName = '' 
        return "<RequireImportErr %s require to import %s first>" % (fileName, str(self.reference))
    

class HdlContext(NonRedefDict):
    """
    Context of hdl, contains all hdl objects hidden behind references
    """
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        
        self.entities = NonRedefDict()
        self.architectures = []
        self.packages = NonRedefDict()
        self.fileInfo = None
        
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
                self[toImport.name] = toImport
        except KeyError:
            raise RequireImportErr(ref)
        
    def lookupGlobal(self, ref):
        """
        lookup reference upside down
        """
        p = self
        n = ref.names[0]  # [TODO]
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
        """[DEPRECATED]
        lookup only in this context
        """
        p = self
        n = locRef.names[-1]  # [TODO]
        while p is not None:
            try:
                return p[n]
            except KeyError:
                p = p.parent
        
        raise KeyError("Identificator %s not defined" % n)
    
    def insertObj(self, obj, caseSensitive, hierarchyOnly=False):
        """
        insert Entity, PackageHeader or Architecture in this context
        """
        from hwt.hdlObjects.package import PackageHeader  # [TODO] rm dependency
        def getName():
            n = obj.name
            if not caseSensitive:
                n = n.lower() 
            return n
        
        def insert(n):
            self.insert(HdlRef([n], caseSensitive), obj)
        
        if isinstance(obj, Entity):
            n = getName()
            self.entities[n] = obj
            insert(n)
        elif  isinstance(obj, RtlSignalBase):
            self[obj._name] = obj
        elif isinstance(obj, PackageHeader):
            n = getName()
            self.packages[n] = obj
            insert(n)
            
        elif isinstance(obj, Architecture):
            self.architectures.append(obj)
            
        elif isinstance(obj, Function):
            # functions are stored in FunctionContainer object
            n = getName()
            try:
                cont = self[n]
            except KeyError:
                cont = FunctionContainer(n, self)
                self.insert(HdlRef([n], caseSensitive), cont)
            cont.append(obj, suppressRedefinition=hierarchyOnly)
        else:
            raise NotImplementedError()
    
    def insert(self, ref, val):
        """
        insert any reference
        """
        c = self
        # for all names create or reuse hiearchy
        for n in ref.names[:-1]:
            c = c.setdefault(n, HdlContext(n, c))
        # store actual object at the end of hierarhy
        c[ref.names[-1]] = val
    
    def copyFrom(self, other):
        """
        copy everything from other HdlContext
        """
        for _, v in other.items():
            self.insertObj(v)
        self.parent = other.parent
        self.name = other.name
               
    def __str__(self):
        return "\n".join([
                    "\n".join([str(e) for _, e in self.entities.items()]),
                    "\n".join([str(a) for a in self.architectures]),
                    "\n".join([str(p) for p in self.packages]),
                    ])