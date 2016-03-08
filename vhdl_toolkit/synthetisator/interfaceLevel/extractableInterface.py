from python_toolkit.arrayQuery import single, NoValueExc
from python_toolkit.stringUtils import matchIgnorecase
from vhdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION

class InterfaceIncompatibilityExc(Exception):
    pass

class ExtractableInterface():
    @classmethod
    def _extractPossiblePrefixes(cls, entity, prefix=""):
        """
        @return: iterator over unit ports witch probably matches with this interface
        """        
        assert(cls._isBuild())
        
        firstIntfNames = []
        if cls._subInterfaces:
            parent = cls
            child = cls
            # construct prefix
            while child._subInterfaces:
                parent = child
                _childName, child = list(child._subInterfaces.items())[0]
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
            o = cls()
            name = o._name
            
        for n in o._alternativeNames:
            firstIntfNames.append(prefix + n)
        firstIntfNames.append(prefix + name)
            
        for firstIntfName in firstIntfNames:
            for p in entity.port:
                if not hasattr(p, "_interface") and p.name.lower().endswith(firstIntfName):
                    # cut off prefix
                    nameLen = len(firstIntfName)
                    if nameLen == 0:
                        yield p.name
                    else:
                        yield p.name[:-nameLen]
                
    def _unExtrac(self):
        """Revent extracting process for this interface"""
        if self._subInterfaces:
            for _, intfConfMap in self._subInterfaces.items():
                intfConfMap._unExtrac()
        else:
            if hasattr(self, "_originEntityPort"):
                if hasattr(self._originEntityPort, "_interface"):
                    del self._originEntityPort._interface
                del self._originEntityPort
                del self._originSigLvlUnit
                
    def _tryToExtractByName(self, prefix, sigLevelUnit):
        """
        @return: self if extraction was successful
        @raise InterfaceIncompatibilityExc: if this interface with this prefix does not fit to this entity 
        """
        if self._subInterfaces:
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
            if allDirMatch:
                self._direction = INTF_DIRECTION.MASTER
            elif noneDirMatch:
                self._direction = INTF_DIRECTION.SLAVE
            else:
                self._unExtrac()
                raise InterfaceIncompatibilityExc("Direction mismatch")
        
        else:
            intfNames = []
            if hasattr(self, "_name"):
                intfNames.append(self._name)
            intfNames.extend(self._alternativeNames)
            for n in intfNames:
                name = prefix + n
                try:
                    self._originEntityPort = single(sigLevelUnit.entity.port,
                                            lambda p : matchIgnorecase(p.name, name))
                    break
                except NoValueExc as e:
                    pass
            if not hasattr(self, "_originEntityPort"):
                self._unExtrac()
                raise  InterfaceIncompatibilityExc("Missing " + prefix + n)

            self._originEntityPort._interface = self
            self._originSigLvlUnit = sigLevelUnit
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
                yield (name, intf) 
            except InterfaceIncompatibilityExc as e:
                #print(e)
                pass
