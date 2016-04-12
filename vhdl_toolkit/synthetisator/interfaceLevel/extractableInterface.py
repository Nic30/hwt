from python_toolkit.arrayQuery import single, NoValueExc
from python_toolkit.stringUtils import matchIgnorecase
from vhdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION
from vhdl_toolkit.hdlObjects.expr import ExprComparator
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.synthetisator.interfaceLevel.interfaceArray import InterfaceArray
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
from vhdl_toolkit.hdlObjects.operatorDefs import AllOps

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


class ExtractableInterface(InterfaceArray):

    @classmethod
    def _extractPossiblePrefixes(cls, entity, prefix=""):
        """
        @return: iterator over unit ports witch probably matches with this interface
        """        
        assert(cls._isBuild())
        
        firstIntfNames = []
        if cls._subInterfaces:
            # find first signal in this interface
            parent = cls
            child = cls
           
            while child._subInterfaces:
                parent = child
                _childName, child = list(child._subInterfaces.items())[0]
                # update prefix
                if child._subInterfaces:
                    if prefix == '':
                        prefix = _childName
                    else:
                        prefix += (parent.NAME_SEPARATOR + _childName)
                else:
                    if prefix != '':
                        prefix += parent.NAME_SEPARATOR
                    
            o = child
            name = _childName
        else:
            # find this interface because it is signal
            o = cls()
            name = o._name
            
        # search for alternative names as well    
        for n in o._alternativeNames:
            firstIntfNames.append(prefix + n)
        firstIntfNames.append(prefix + name)
        
        # search ports names for firstIntfNames  
        for firstIntfName in firstIntfNames:
            for p in entity.ports:
                if not hasattr(p, "_interface") and p.name.lower().endswith(firstIntfName):
                    # cut off prefix
                    nameLen = len(firstIntfName)
                    if nameLen == 0:
                        yield p.name
                    else:
                        yield p.name[:-nameLen]
                
    def _unExtrac(self):
        """undo extracting process for this interface"""
        if self._subInterfaces:
            for _, intfConfMap in self._subInterfaces.items():
                intfConfMap._unExtrac()
        else:
            if hasattr(self, "_originEntityPort"):
                if hasattr(self._originEntityPort, "_interface"):
                    del self._originEntityPort._interface
                del self._originEntityPort
                del self._originSigLvlUnit
                
    def _extractDtype(self, multipliedBy=None):
        if self._subInterfaces:
            for _, si in self._subInterfaces.items():
                si._extractDtype(multipliedBy=multipliedBy)
        else:
            # update interface type from hdl, update generics
            try:
                intfTConstr = self._originalIntfDtype.constrain
            except AttributeError:  
                intfTConstr = self._dtype.constrain
            if intfTConstr is not None:
                
                unitTConstr = self._originEntityPort.dtype.constrain
                 
                for intfParam, unitParam in ExprComparator\
                                            .findExprDiffInParam(intfTConstr, unitTConstr):
                    if multipliedBy is not None and isinstance(unitParam, Signal):
                        mulOp = unitParam.singleDriver()
                        assert(mulOp.operator == AllOps.MUL)
                        op0 = mulOp.ops[0]
                        op1 = mulOp.ops[1]
                        
                        if type(op0) == type(multipliedBy) and op0 == multipliedBy:
                            updateParam(intfParam, op1)
                        else:
                            assert(type(op1) == type(multipliedBy) and op1 == multipliedBy)
                            updateParam(intfParam, op0)
                    else:
                        updateParam(intfParam, unitParam)
            if not hasattr(self, "_originalIntfDtype"):
                self._originalIntfDtype = self._dtype
                self._dtype = self._originEntityPort.dtype
        
    def _tryToExtractByName(self, prefix, sigLevelUnit):
        """
        @return: self if extraction was successful
        @raise InterfaceIncompatibilityExc: if this interface with this prefix does not fit to this entity 
        """
        if self._subInterfaces:
            # extract subinterfaces and propagate params
            allDirMatch = True
            noneDirMatch = True
            if hasattr(self, "_name") and self._name != '':
                prefix += self._name + self.NAME_SEPARATOR
            try:
                for intfName, intf in self._subInterfaces.items():
                    assert(intf._name == intfName)
                    intf._tryToExtractByName(prefix, sigLevelUnit)
                    if intf._subInterfaces:
                        dirMatches = intf._direction == INTF_DIRECTION.MASTER
                    else:
                        dirMatches = intf._originEntityPort.direction == intf._masterDir
                    allDirMatch = allDirMatch and dirMatches
                    noneDirMatch = noneDirMatch  and not dirMatches     
            except InterfaceIncompatibilityExc as e:
                for intfName, intf in self._subInterfaces.items():
                    intf._unExtrac()
                raise e
            
            # update all params on this interface
            for pName, p in self._params.items():
                if p.replacedWith is not None:
                    setattr(self, pName, p.replacedWith)
                    self._params[pName] = p.replacedWith
                
            if allDirMatch:
                self._direction = INTF_DIRECTION.MASTER
            elif noneDirMatch:
                self._direction = INTF_DIRECTION.SLAVE
            else:
                self._unExtrac()
                raise InterfaceIncompatibilityExc("Direction mismatch")
        
            # update all params which were found in unit
            # update params on object as well
            for pName, p in self._params.items():
                if not p.replacedWith is None:
                    self._addParam(pName, p.replacedWith, allowUpdate=True)
            
        else:
            # extract signal(Ap_none , etc.)
            # collect all posible names
            intfNames = []
            if hasattr(self, "_name"):
                intfNames.append(self._name)
            intfNames.extend(self._alternativeNames)
            # try find suitable portItem in entity port 
            for n in intfNames:
                name = prefix + n
                try:
                    self._originEntityPort = single(sigLevelUnit.entity.ports,
                                            lambda p : matchIgnorecase(p.name, name))
                    break
                except NoValueExc as e:
                    pass
            if not hasattr(self, "_originEntityPort"):
                self._unExtrac()
                raise  InterfaceIncompatibilityExc("Missing " + prefix + n)

            self._extractDtype()
            
            # assign references to hdl objects
            self._originEntityPort._interface = self
            self._originSigLvlUnit = sigLevelUnit
            # resolve direction
            dirMatches = self._originEntityPort.direction == self._masterDir
            if dirMatches:
                self._direction = INTF_DIRECTION.MASTER
            else:
                self._direction = INTF_DIRECTION.SLAVE

        return self
    
    @classmethod        
    def _tryToExtract(cls, sigLevelUnit):
        """
        @return: iterator over tuples (interface name. extracted interface)
        """
        cls._builded()
        for name in cls._extractPossiblePrefixes(sigLevelUnit.entity):
            try:
                # print("\n_tryToExtract 1 ", name, cls)
                intfInst = cls(isExtern=True)
                prefix = name 
                # if cls._subInterfaces: 
                #    prefix = name + cls.NAME_SEPARATOR
                # else:
                #    prefix = name
                     
                intf = intfInst._tryToExtractByName(prefix, sigLevelUnit)
                if not intf._subInterfaces:
                    name += intf._name
                if name.endswith("_"):
                    name = name[:-1]
                # print(("_tryToExtract", name, intf))
                
                # if interface is actually array of interfaces extract the size of this array 
                mf = intf._tryExtractMultiplicationFactor()
                if mf is not None:
                    intf._extractDtype(multipliedBy=mf)
                    intf._setMultipliedBy(mf, updateTypes=False)
                    
                yield (name, intf) 
            except InterfaceIncompatibilityExc as e:
                # pass if intrface does not match the interface on sigLevelUnit
                # print(e)
                pass
