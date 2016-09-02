from hdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION
from hdl_toolkit.synthesizer.interfaceLevel.unit import Unit
from hdl_toolkit.synthesizer.exceptions import IntfLvlConfErr

def setOut(*interfaces, defVal=None):
    """
    set interfaces as output interfaces
    @attention: only for instances of EmptyUnit
    """
    for i in interfaces:
        i._setDirectionsLikeIn(INTF_DIRECTION.SLAVE)
        
class EmptyUnit(Unit):
    """
    Unit used for prototyping all output interfaces are connected to _defaultValue
    and this is only think which architecture contains
    
    @cvar _defaultValue: this value is used to initialize all signals 
    """
    _defaultValue = None
    def _toRtl(self):
        self._initName()
        for i in self._interfaces:
            i._setDirectionsLikeIn(INTF_DIRECTION.MASTER)
        
        
        self._loadMyImplementations()
        # construct globals (generics for entity)
        cntx = self._contextFromParams()
        externInterf = [] 
        # prepare connections     
        for i in self._interfaces:
            signals = i._signalsForInterface(cntx)
            if not i._isExtern:
                raise IntfLvlConfErr("All interfaces in EmptyUnit has to be extern, %s: %s is not" % 
                                     (self.__class__.__name__, i._getFullName()))
            externInterf.extend(signals)
            #i._resolveDirections()
            # connect outputs to dummy value
            for s in signals:
                if s._interface._direction == INTF_DIRECTION.SLAVE:
                    s._assignFrom(s._dtype.fromPy(self._defaultValue))
        if not externInterf:
            raise  Exception("Can not find any external interface for unit " + self._name \
                              + "- there is no such a thing as unit without interfaces")
        yield  from self._synthetiseContext(externInterf, cntx)
        # self._checkEntityPortDirections()
