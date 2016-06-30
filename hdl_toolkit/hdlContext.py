#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from myhdl.conversion._toVHDL import _shortversion

from hdl_toolkit.hdlObjects.reference import HdlRef 
from hdl_toolkit.nonRedefDict import NonRedefDict
from hdl_toolkit.hdlObjects.entity import Entity
from hdl_toolkit.hdlObjects.architecture import Architecture
from hdl_toolkit.hdlObjects.function import Function
from hdl_toolkit.hdlObjects.functionContainer import FunctionContainer
from hdl_toolkit.synthetisator.rtlLevel.mainBases import RtlSignalBase
from hdl_toolkit.hdlObjects.types.defs import BOOL, INT, STR, BIT
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.integer import Integer



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
    
class HDLParseErr(Exception):
    pass

class HDLCtx(NonRedefDict):
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
        from hdl_toolkit.hdlObjects.package import PackageHeader  # [TODO] rm dependency
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
            c = c.setdefault(n, HDLCtx(n, c))
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

class FakeStd_logic_1164():
    """mock of Std_logic_1164 from vhdl"""
    std_logic_vector = Bits(forceVector=True)
    std_logic_vector_ref = HdlRef(["ieee", "std_logic_1164", "std_logic_vector"], False)
    std_ulogic_vector_ref = HdlRef(["ieee", "std_logic_1164", "std_ulogic"], False)
    
    std_logic_unsigned_sub_ref = HdlRef(["ieee", "std_logic_unsigned", "-"], False)
    std_logic_unsigned_sub = FunctionContainer('-', None)

    std_logic = BIT
    std_logic_ref = HdlRef(["ieee", "std_logic_1164", "std_logic"], False)
    
    signed_ref = HdlRef(["ieee", "numeric_std", 'signed'], False)
    signed = Bits(signed=True)

    unsigned_ref = HdlRef(["ieee", "numeric_std", 'unsigned'], False)
    unsigned = Bits(signed=False)
    
    resize_ref = HdlRef(["ieee", "numeric_std", 'resize'], False)
    resize = FunctionContainer('resize', None)

class FakeMyHdl():
    p_name = "pck_myhdl_%s" % _shortversion
    package_ref = HdlRef(["work", p_name ], False)
    package_fake = HDLCtx(p_name, None)

class BaseVhdlContext():
    integer = INT
    natural = Integer(_min=0)
    positive = Integer(_min=1)
    boolean = BOOL
    string = STR
    
   
    @classmethod
    def importFakeLibs(cls, ctx):
        BaseVhdlContext.importFakeIEEELib(ctx)
        BaseVhdlContext.importFakeTextIo(ctx)
        ctx.insert(FakeMyHdl.package_ref, FakeMyHdl.package_fake)
        
    @classmethod
    def importFakeTextIo(cls, ctx):
        ctx.insert(HdlRef(['std', 'textio', 'read'], False), None)

    @classmethod 
    def importFakeIEEELib(cls, ctx):
        f = FakeStd_logic_1164
        ctx.insert(f.std_logic_vector_ref, f.std_logic_vector)
        ctx.insert(f.std_ulogic_vector_ref, f.std_logic_vector)
        ctx.insert(f.std_logic_ref, f.std_logic)
        ctx.insert(HdlRef(['ieee', 'std_logic_unsigned', 'conv_integer'], False), None)
        ctx.insert(HdlRef(['ieee', 'std_logic_arith', 'is_signed'], False), None)
        ctx.insert(HdlRef(["ieee", "std_logic_misc", "and_reduce"], False), None)
        ctx.insert(f.std_logic_unsigned_sub_ref, f.std_logic_unsigned_sub)
        ctx.insert(f.signed_ref, f.signed)
        ctx.insert(f.unsigned_ref, f.unsigned)
        ctx.insert(f.resize_ref, f.resize)
    
    @classmethod
    def getBaseCtx(cls):
        d = HDLCtx(None, None)
        for t in [cls.integer, cls.positive, cls.natural,
                   cls.boolean, cls.string]:
            d[t.name.lower()] = t
        d['true'] = BOOL.fromPy(True)
        d['false'] = BOOL.fromPy(False)
        return d

class BaseVerilogContext():
    integer = INT
    string = STR
    wire = Bits()
   
    @classmethod
    def importFakeLibs(cls, ctx):
        pass

    @classmethod
    def getBaseCtx(cls):
        d = HDLCtx(None, None)
        d['integer'] = cls.integer
        d['__str__'] = cls.string
        d['wire'] = cls.wire
        return d
