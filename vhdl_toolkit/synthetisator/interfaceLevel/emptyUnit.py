from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit, defaultUnitName
from vhdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION, INTF_DIRECTION


def _setOutIntf(intf):
    intf._direction = INTF_DIRECTION.SLAVE
    if not hasattr(intf, "_interfaces"):
        raise AttributeError("%s has not attribute _interfaces use this function after declaration of interface" % (repr(intf)))
    for i in intf._interfaces:
        _setOutIntf(i)

def setOut(*intfs):
    for intf in intfs:
        _setOutIntf(intf)

class EmptyUnit(Unit):
    """
    Unit used for prototyping all output interfaces are connected to _defaultValue
    and this is only think which architecture contains
    
    @cvar _defaultValue: this value is used to initialize all signals 
    """
    _defaultValue = None
    def _toRtl(self):
        self._initName()
        self._loadMyImplementations()
        # construct globals (generics for entity)
        cntx = self._contextFromParams()
        externInterf = [] 
        # prepare connections     
        for connection in self._interfaces:
            connectionName = connection._name
            signals = connection._signalsForInterface(cntx, connectionName)
            if not connection._isExtern:
                raise IntfLvlConfErr("All interfaces in BlackBox has to be extern, %s: %s is not" % 
                                     (self.__class__.__name__, connection._getFullName()))
            externInterf.extend(signals)
            # connect outputs to dummy value
            for s in signals:
                if s._interface._getSignalDirection() == DIRECTION.IN:
                    s.assignFrom(Value.fromPyVal(self._defaultValue, s.dtype))
        if not externInterf:
            raise  Exception("Can not find any external interface for unit " + self._name \
                              + "- there is no such a thing as unit without interfaces")
        yield  from self._synthetiseContext(externInterf, cntx)