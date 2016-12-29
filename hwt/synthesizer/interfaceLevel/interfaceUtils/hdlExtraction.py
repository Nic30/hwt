from hwt.hdlObjects.expr import ExprComparator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.constants import INTF_DIRECTION
from hwt.hdlObjects.types.sliceVal import SliceVal
from hwt.hdlObjects.value import Value
from hwt.synthesizer.interfaceLevel.interfaceUtils.array import InterfaceArray
from hwt.synthesizer.param import Param
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.walkers import walkSignalsInExpr
from hwt.pyUtils.arrayQuery import single, NoValueExc, arr_any
from hwt.pyUtils.stringUtils import matchIgnorecase


class InterfaceIncompatibilityExc(Exception):
    pass

def updateParam(intfParam, unitParam):
    if isinstance(unitParam, Param):
        intfParam.replace(unitParam)
    elif isinstance(unitParam, Value):
        intfParam.set(unitParam)
    else:
        # parameter resolution was not successful
        pass
    
def typeIsParametrized(dtype):
    c = dtype.constrain
    if c is None:
        return False
    else:
        return arr_any(list(walkSignalsInExpr(c)), lambda x: True)

class ExtractableInterface(InterfaceArray):

    @classmethod
    def _extractPossiblePrefixes(cls, ports, prefix=""):
        """
        @return: iterator over unit ports witch probably matches with this interface
        """
        intfObj = cls()
        intfObj._loadDeclarations()
        
        # find first signal in this interface
        parent = intfObj
        child = intfObj
        
        while child._interfaces:
            parent = child
            child = child._interfaces[0]
            # update prefix
            if child._interfaces:
                if prefix == '':
                    prefix = child._name
                else:
                    prefix += (parent._NAME_SEPARATOR + child._name)
            else:
                if prefix != '':
                    prefix += parent._NAME_SEPARATOR
                
        o = child
        name = child._name
            
        # search for alternative names as well    
        firstIntfNames = []
        for n in o._alternativeNames:
            firstIntfNames.append(prefix + n)
        firstIntfNames.append(prefix + name)
        
        # search ports names for firstIntfNames  
        for firstIntfName in firstIntfNames:
            for p in ports:
                if not hasattr(p, "_interface") and p.name.lower().endswith(firstIntfName):
                    # cut off prefix
                    nameLen = len(firstIntfName)
                    if nameLen == 0:
                        yield p.name
                    else:
                        yield p.name[:-nameLen]
                
    def _unExtrac(self):
        """undo extracting process for this interface"""
        if self._interfaces:
            for intfConfMap in self._interfaces:
                intfConfMap._unExtrac()
        else:
            if hasattr(self, "_boundedEntityPort"):
                if hasattr(self._boundedEntityPort, "_interface"):
                    del self._boundedEntityPort._interface
                del self._boundedEntityPort
                
    def _extractDtype(self, multipliedBy=None):
        """
        Compare signal _dtype and _dtype of interface declaration and try match parameters
        """
        self._multipliedBy = multipliedBy
        if self._interfaces:
            for si in self._interfaces:
                si._extractDtype(multipliedBy=multipliedBy)
        else:
            # update interface type from hdl, update generics
            intfTConstr = self._dtype.constrain

            if intfTConstr is not None and isinstance(intfTConstr, (RtlSignalBase, SliceVal)):
                unitTConstr = self._boundedEntityPort._dtype.constrain
                paramDiff = list(ExprComparator.findExprDiffInParam(intfTConstr, unitTConstr))
                    
                for intfParam, unitParam in paramDiff:
                    if multipliedBy is not None and isinstance(unitParam, RtlSignalBase):
                        mulOp = unitParam.singleDriver()
                        assert mulOp.operator == AllOps.MUL
                        op0 = mulOp.ops[0]
                        op1 = mulOp.ops[1]
                        
                        if type(op0) == type(multipliedBy) and op0 == multipliedBy:
                            _unitParam = op1
                        else:
                            assert type(op1) == type(multipliedBy) and op1 == multipliedBy
                            _unitParam = op0
                    else:
                        assert multipliedBy is None
                        _unitParam = unitParam 

                if len(paramDiff) == 0:
                    # [TODO] and port is not parametrized
                    origT = self._boundedEntityPort._dtype
                    t = self._dtype
                    self._dtypeMatch = origT == t and not typeIsParametrized(origT) and not typeIsParametrized(t) 
                else:
                    self._dtypeMatch = isinstance(_unitParam, (Param, Value))
                    updateParam(intfParam, _unitParam)
            else:
                self._dtypeMatch = self._boundedEntityPort._dtype == self._dtype
        
    def _tryToExtractByName(self, prefix, ports):
        """
        @return: self if extraction was successful
        @raise InterfaceIncompatibilityExc: if this interface with this prefix does not fit for this entity 
        """
        if self._interfaces:
            # extract subinterfaces and propagate params
            allDirMatch = True
            noneDirMatch = True
            if hasattr(self, "_name") and self._name != '':
                prefix += self._name + self._NAME_SEPARATOR
            try:
                for intf in self._interfaces:
                    intf._tryToExtractByName(prefix, ports)
                    if intf._interfaces:
                        dirMatches = intf._direction == INTF_DIRECTION.MASTER
                    else:
                        dirMatches = intf._boundedEntityPort.direction == intf._masterDir
                    allDirMatch = allDirMatch and dirMatches
                    noneDirMatch = noneDirMatch  and not dirMatches     
            except InterfaceIncompatibilityExc as e:
                for intf in self._interfaces:
                    intf._unExtrac()
                raise e
            
                
            if allDirMatch:
                self._direction = INTF_DIRECTION.MASTER
            elif noneDirMatch:
                self._direction = INTF_DIRECTION.SLAVE
            else:
                self._unExtrac()
                raise InterfaceIncompatibilityExc("Direction mismatch")
        
        else:
            # extract signal(Signal , etc.)
            # collect all possible names
            intfNames = []
            if hasattr(self, "_name"):
                intfNames.append(self._name)
            intfNames.extend(self._alternativeNames)
            # try find suitable portItem in entity port 
            for n in intfNames:
                name = prefix + n
                try:
                    self._boundedEntityPort = single(ports,
                                            lambda p : matchIgnorecase(p.name, name))
                    break
                except NoValueExc as e:
                    continue
            if not hasattr(self, "_boundedEntityPort"):
                self._unExtrac()
                raise  InterfaceIncompatibilityExc("Missing " + prefix + n)

            self._extractDtype()
            
            # assign references to hdl objects
            self._boundedEntityPort._interface = self
            # resolve direction
            dirMatches = self._boundedEntityPort.direction == self._masterDir
            if dirMatches:
                self._direction = INTF_DIRECTION.MASTER
            else:
                self._direction = INTF_DIRECTION.SLAVE

        return self
    
    @classmethod        
    def _tryToExtract(cls, ports):
        """
        @return: iterator over tuples (interface name. extracted interface)
        """
        # [TODO] ports as dict
        for name in cls._extractPossiblePrefixes(ports):
            try:
                intfInst = cls()
                intfInst._loadDeclarations()
                prefix = name 
                     
                intf = intfInst._tryToExtractByName(prefix, ports)
                if name == "":
                    if intf._interfaces:
                        name = cls.__name__.lower()
                    else:
                        name = intf._boundedEntityPort.name
                else:
                    name += intf._name
                
                if name.endswith("_"):
                    name = name[:-1]
                
                if intf._interfaces:  # if is possible to determine size of this potential intf. array 
                    # if interface is actually array of interfaces extract the size of this array 
                    mf = intf._tryExtractMultiplicationFactor()
                    if mf is not None:
                        intf._extractDtype(multipliedBy=mf)
                        intf._setMultipliedBy(mf, updateTypes=False)
                intfInst._setAsExtern(True)
                yield (name, intf) 
            except InterfaceIncompatibilityExc as e:
                # pass if interface was not found in ports
                pass
