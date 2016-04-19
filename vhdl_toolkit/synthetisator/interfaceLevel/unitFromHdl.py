import inspect, os
import types
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.hdlObjects.operator import Operator
from vhdl_toolkit.hdlObjects.function import FnContainer
from vhdl_toolkit.parser_utils import entityFromFile, loadCntxWithDependencies
from vhdl_toolkit.hdlContext import RequireImportErr
from vhdl_toolkit.synthetisator.rtlLevel.unit import VHDLUnit
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal, SignalNode
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.synthetisator.interfaceLevel.unitUtils import defaultUnitName, walkSignalOnUnit
from vhdl_toolkit.synthetisator.interfaceLevel.interfaceUtils import walkPhysInterfaces
from vhdl_toolkit.interfaces.all import allInterfaces

def cloneExprWithUpdatedParams(expr, paramUpdateDict):
    if isinstance(expr, Param):
        return paramUpdateDict[expr]
    elif isinstance(expr, Value):
        return expr.clone()
    elif isinstance(expr, Signal):
        d = expr.singleDriver()
        assert(isinstance(d, Operator))
        ops = [ cloneExprWithUpdatedParams(x, paramUpdateDict) for x in d.ops]
        o = Operator(d.operator, ops)
        return SignalNode.resForOp(o)
    elif isinstance(expr, FnContainer):
        return expr
    else:
        raise NotImplementedError("Not implemented for %s" % (repr(expr)))

class UnitFromHdl(Unit):
    """
    @cvar _hdlSources:  str or list of hdl filenames, they can be relative to file 
        where is *.py file stored and they are automaticaly converted to absolute path
        first entity in first file is taken as interface template for this unit
        this is currently supported only for vhdl
    @cvar _intfClasses: interface classes which are searched on hdl entity 
    """
    def __init__(self, intfClasses=allInterfaces, debugParser=False):
        self.__class__._intfClasses = intfClasses
        self.__class__._debugParser = debugParser
        super(UnitFromHdl, self).__init__()
    
    def _config(self):
        cls = self.__class__
        self._params = []
        self._interfaces = []
        self._paramsOrigToInst = {}

        for p in cls._params:
            instP = Param(p.defaultVal)
            setattr(self, p.name, instP)
            
    def _declr(self):
        cls = self.__class__
        for p in cls._params:
            self._paramsOrigToInst[p] = getattr(self, p.name)
            
        for i in cls._interfaces:
            instI = i.__class__(loadConfig=False)
            instI._isExtern = i._isExtern 
            instI._direction = i._direction
            instI._origI = i
            def configFromExtractedIntf(instI):
                for p in instI._origI._params:
                    if p.replacedWith:
                        pName = p.replacedWith.name
                        instP = getattr(self, pName)
                        setattr(instI, p.name, instP)
                    else:
                        # parameter was not found
                        instV = p.defaultVal.clone()
                        instV.vldMask = 0
                        setattr(instI, p.name, Param(instV))
                
                # set array size
                mulBy = instI._origI._multipliedBy
                if isinstance(mulBy, Param):
                    mulBy = self._paramsOrigToInst[mulBy]
                instI._multipliedBy = mulBy   
                    
                             
            # overload _config function
            instI._config = types.MethodType(configFromExtractedIntf, instI)
            instI._loadConfig()
                  
            instI._origLoadDeclarations = instI._loadDeclarations
            def declarationsFromExtractedIntf(instI):
                instI._origLoadDeclarations()
                for iSig, instISig in zip(walkPhysInterfaces(instI._origI), walkPhysInterfaces(instI)):
                    instISig._originEntityPort = iSig._originEntityPort
                    if not iSig._dtypeMatch:
                        origT = iSig._originEntityPort.dtype
                        if origT.constrain is None:
                            newT = origT.__class__()
                        else:
                            newT = origT.__class__(cloneExprWithUpdatedParams(origT.constrain, self._paramsOrigToInst))  
                        instISig._dtype = newT
            # overload _loadDeclarations function
            instI._loadDeclarations = types.MethodType(declarationsFromExtractedIntf, instI) 
            
            setattr(self, i._name, instI)
        
            

    @classmethod
    def _build(cls):
        # convert source filenames to absolute paths
        assert(cls._hdlSources)
        if isinstance(cls._hdlSources, str):
            cls._hdlSources = [cls._hdlSources]
        baseDir = os.path.dirname(inspect.getfile(cls))
        cls._hdlSources = [os.path.join(baseDir, s) for s in cls._hdlSources]

        # init hdl object containers on this unit       
        cls._params = []
        cls._interfaces = []
        cls._units = []

        # extract params from entity generics
        try:
            cls._entity = entityFromFile(cls._hdlSources[0], debug=cls._debugParser)
        except RequireImportErr:
            ctx = loadCntxWithDependencies(cls._hdlSources, debug=cls._debugParser)
            ents = ctx.entities
            assert(len(ents) == 1)
            cls._entity = ents[list(ents.keys())[0]]
            
        for g in cls._entity.generics:
            # if hasattr(cls, g.name):
            #    raise  Exception("Already has param %s (old:%s , new:%s)" 
            #          % (g.name, str(getattr(cls, g.name)), str(g)))
            cls._params.append(g)

        # lookup all interfaces
        for intfCls in cls._intfClasses:
            for intfName, interface in intfCls._tryToExtract(cls._entity.ports):
                # if hasattr(cls, intfName):
                #    raise  Exception("Already has interface %s (old:%s , new:%s)" 
                #                     % (intfName, str(getattr(cls, intfName)), str(interface)))
                interface._name = intfName
                cls._interfaces.append(interface)
                interface._setAsExtern(True)

        for p in cls._entity.ports:
            # == loading testbenches is not supported by this class 
            if not (hasattr(p, '_interface') and p._interface is not None):
                raise AssertionError("Port %s does not have any interface assigned" % (p.name))  # every port should have interface (Ap_none at least) 
  
        
        cls._clsBuildFor = cls
    
    def _synthesise(self, name=None):
        """Convert unit to hdl objects"""
        assert(self._entity)
        self._name = defaultUnitName(self, name)
        self._sigLvlUnit = VHDLUnit(self._entity)
        for s in walkSignalOnUnit(self):
            s._originSigLvlUnit = self._sigLvlUnit
            
        return [self]

    def __str__(self):
        return "\n".join(['--%s' % (s) for s in self._hdlSources])
