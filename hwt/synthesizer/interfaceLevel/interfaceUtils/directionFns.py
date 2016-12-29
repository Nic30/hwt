from hwt.hdlObjects.constants import INTF_DIRECTION, DIRECTION
from hwt.synthesizer.exceptions import IntfLvlConfErr


class InterfaceDirectionFns():

    def _setDirectionsLikeIn(self, intfDir):
        # [TODO] array elements
        d = DIRECTION.asIntfDirection(self._masterDir)
        if intfDir == INTF_DIRECTION.MASTER or d == INTF_DIRECTION.TRISTATE:
            self._direction = d
            for i in self._interfaces:
                i._setDirectionsLikeIn(d)
        else:
            opDir = INTF_DIRECTION.opposite(d)
            self._direction = opDir
            for i in self._interfaces:
                i._setDirectionsLikeIn(opDir)
        
    def __directionProbe(self):
        if not self._interfaces:
            s = self._sig
            d = self._masterDir
            return (not bool(s.drivers), bool(s.drivers))
        
        allInMasterConf = True
        allInSlaveConf = True
        for i in self._interfaces:
            i._resolveDirections(updateDir=False)
            d = i._direction
            md = DIRECTION.asIntfDirection(i._masterDir)
            if d != INTF_DIRECTION.UNKNOWN:
                isLikeInM = d == md
                isLikeInS = d == INTF_DIRECTION.opposite(md)
                allInMasterConf = allInMasterConf and isLikeInM
                allInSlaveConf = allInSlaveConf and isLikeInS
        return  (allInMasterConf, allInSlaveConf)  
            
    def _resolveDirections(self, updateDir=True):
        allM, allS = self.__directionProbe()
        
        if allM and allS and self._arrayElemCache:  # if direction is nod clear from this intf. and it has elems.
            allM, allS = self._arrayElemCache[0].__directionProbe()

        if allM and allS:
            self._direction = INTF_DIRECTION.UNKNOWN
        elif allM:
            self._direction = INTF_DIRECTION.MASTER
        elif allS:
            self._direction = INTF_DIRECTION.SLAVE
        else:
            raise IntfLvlConfErr("Subinterfaces on %s \nhave not consistent directions\n%s" % 
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
    
    def _setDirLock(self, dirLock):
        self._dirLocked = dirLock
        for intf in self._interfaces:
            intf._setDirLock(dirLock)
    
    def _reverseDirection(self):
        """Reverse direction of this interface in implementation stage"""
        if self._dirLocked:
            raise IntfLvlConfErr("Can not reverse direction on interface %s because it was locked (%s)" % 
                                 (repr(self), self._direction))
        self._direction = INTF_DIRECTION.opposite(self._direction)
        for intf in self._interfaces:
            intf._reverseDirection()
