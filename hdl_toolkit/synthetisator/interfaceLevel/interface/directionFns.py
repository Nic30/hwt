from hdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from hdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION, DIRECTION
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase


class InterfaceDirectionFns():
    def _setSrc(self, src):
        """Set driver in implementation stage"""
        assert(self._isAccessible)
        srcCls = src.__class__
        selfCls = self.__class__
        assert(issubclass(selfCls, src.__class__) or issubclass(srcCls, selfCls))  # assert intf classes are related
        if self._src is not None:
            raise IntfLvlConfErr(
                "Interface %s already has driver (%s) and can not be connected to other driver (%s)" % 
                (repr(self), repr(self._src), repr(src)))
        self._src = src
    
    def _setDirectionsLikeIn(self, intfDir):
        # [TODO] array elements
        d = DIRECTION.asIntfDirection(self._masterDir)
        if intfDir == INTF_DIRECTION.MASTER:
            self._direction = d
            for i in self._interfaces:
                i._setDirectionsLikeIn(d)
        else:
            opDir = INTF_DIRECTION.oposite(d)
            self._direction = opDir
            for i in self._interfaces:
                i._setDirectionsLikeIn(opDir)
        
    @staticmethod    
    def __directionProbe(interfaces):
        allInMasterConf = True
        allInSlaveConf = True
        for i in interfaces:
            i._resolveDirections(updateDir=False)
            md = DIRECTION.asIntfDirection(i._masterDir)
            d = i._direction
            if d != INTF_DIRECTION.UNKNOWN:
                isLikeInM = d == md
                isLikeInS = d == INTF_DIRECTION.oposite(md)
                allInMasterConf = allInMasterConf and isLikeInM
                allInSlaveConf = allInSlaveConf and isLikeInS
        return  (allInMasterConf, allInSlaveConf)  
            
    def _resolveDirections(self, updateDir=True):
        """
        if have src -> slave
            check no subinterface has src
            reverse directions because master is default
        else
           check subinterfaces if all of them can be master or slave 
           if all are masters:
               let directions like they are, master is default
           elif all are slaves:
               reverse directions of me 
           
        """
        def assertHasNotSrc(i):
            if i._src is not None:
                raise IntfLvlConfErr("Interface %s has driver %s, but is already driven by parent (%s) driver (%s)" % 
                                     (repr(i), repr(i._src), repr(self), repr(self._src)))
            for si in i._interfaces:
                assertHasNotSrc(si)
            
        if self._src is not None:
            for i in self._interfaces:
                assertHasNotSrc(i)
            self._direction = INTF_DIRECTION.SLAVE
        else:
            allM, allS = InterfaceDirectionFns.__directionProbe(self._interfaces)
            if allM and allS:
                allM, allS = InterfaceDirectionFns.__directionProbe(self._arrayElemCache)

            if allM and allS:
                self._direction = INTF_DIRECTION.UNKNOWN
            elif allM:
                self._direction = INTF_DIRECTION.MASTER
            elif allS:
                self._direction = INTF_DIRECTION.SLAVE
            else:
                raise IntfLvlConfErr("Subinterfaces on %s have not consistent directions\n%s" % 
                        (repr(self), '\n'.join([str((i._direction, repr(i))) for i in self._interfaces])))
        
        
        if updateDir:
            if self._direction == INTF_DIRECTION.UNKNOWN:
                self._direction = INTF_DIRECTION.MASTER
            self._setDirectionsLikeIn(self._direction)
    
    def _setAsExtern(self, isExtern):
        """Set interface as extern"""
        self._isExtern = isExtern
        for prop in self._interfaces:
            prop._setAsExtern(isExtern)
    
    def _propagateSrc(self):
        """Propagate driver in routing"""
        assert(self is not self._src)
        if self._src is not None and isinstance(self._src, InterfaceBase):
            self._src._endpoints.add(self)
        for sIntf in self._interfaces:
            sIntf._propagateSrc()
            
        for e in self._arrayElemCache:
            if e is not None:
                e._propagateSrc()

    def _setDirLock(self, dirLock):
        self._dirLocked = dirLock
        for intf in self._interfaces:
            intf._setDirLock(dirLock)
    
    def _reverseDirection(self):
        """Reverse direction of this interface in implementation stage"""
        if self._dirLocked:
            raise IntfLvlConfErr("Can not reverse direction on interface %s because it was locked (%s)" % 
                                 (repr(self), self._direction))
        self._direction = INTF_DIRECTION.oposite(self._direction)
        for intf in self._interfaces:
            intf._reverseDirection()
