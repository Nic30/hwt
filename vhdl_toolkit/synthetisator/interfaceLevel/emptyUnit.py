from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit, defaultUnitName
from vhdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION


class EmptyUnit(Unit):
    """
    Unit used for prototyping all output interfaces are connected to _defaultValue
    and this is only think which architecture contains
    
    @cvar _defaultValue: this value is used to initialize all signals 
    """
    _defaultValue = None
    def _synthesise(self, name=None):
        name = defaultUnitName(self, name)
        self._name = name
        # construct globals (generics for entity)
        cntx = self._contextFromParams()
        externInterf = [] 
        # prepare connections     
        for connectionName, connection in self._interfaces.items():
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
            raise  Exception("Can not find any external interface for unit " + name \
                              + "- there is no such a thing as unit without interfaces")
        yield  from self._synthetiseContext(externInterf, cntx)