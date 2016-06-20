from hdl_toolkit.hdlObjects.assignment import Assignment
from hdl_toolkit.hdlObjects.types.hdlType import HdlType
from hdl_toolkit.hdlObjects.variables import SignalItem
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.simulator.exceptions import SimNotInitialized, SimException
from hdl_toolkit.hdlObjects.types.defs import BOOL, INT, STR
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.synthetisator.rtlLevel.signal.exceptions import MultipleDriversExc
from hdl_toolkit.synthetisator.rtlLevel.signal.ops import SignalOps


class UniqList(list):
    def append(self, obj):
        if obj in self:
            pass
        return list.append(self, obj)

class Signal(SignalItem, SignalOps):
    """
    more like net
    @ivar _usedOps: dictionary of used operators which can be reused
    """
    def __init__(self, name, dtype, defaultVal=None):
        if name is None:
            name = "sig_" + str(id(self))
            self.hasGenericName = True 
       
        assert(isinstance(dtype, HdlType))
        super(Signal, self).__init__(name, dtype, defaultVal)
        # set can not be used because hash of items are changign
        self.endpoints = UniqList()
        self.drivers = UniqList()
        self._usedOps = {}
        self.negated = False
    
    def simPropagateChanges(self):
        if self._oldVal != self._val or self._oldVal.eventMask != self._val.eventMask:
            conf = self._simulator.config
            env = self._simulator.env
            self._oldVal = self._val
            for e in self.endpoints:
                if conf.log:
                    conf.logger("%d: Signal.simPropagateChanges %s -> %s" % (env.now, self.name, str(e)))
                yield env.process(e.simPropagateChanges())
        
    def staticEval(self):
        # operator writes in self._val new value
        if self.drivers:
            for d in self.drivers:
                d.staticEval()
        else:
                if isinstance(self.defaultVal, Signal):
                        self._val = self.defaultVal._val
                else:
                    if not self._val.vldMask:  # [TODO] find better way how to find out if was initialized
                        self._val = self.defaultVal
        if not isinstance(self._val, Value):
            raise SimException("Evaluation of signal returned not supported object (%s)" % (repr(self._val)))
        return self._val
    
    def simUpdateVal(self, newVal):
        if not  isinstance(newVal, Value):
            raise SimException("new value is instance of %s it should be instance of value" % (str(newVal.__class__)))
        self._val = newVal
        try:
            env = self._simulator.env
        except AttributeError:
            raise SimNotInitialized("Singal %s does not contains reference to its simulator" % (str(self)))
        c = self._simulator.config
        if  c.log:
            c.logger("%d: %s <= %s" % (env.now, self.name, str(newVal)))
        
        yield env.process(self.simPropagateChanges())
     
    def singleDriver(self):
        if len(self.drivers) != 1:
            raise MultipleDriversExc()
        return list(self.drivers)[0]
            
class SyncSignal(Signal):
    def __init__(self, name, var_type, defaultVal=None):
        super().__init__(name, var_type, defaultVal)
        self.next = Signal(name + "_next", var_type, defaultVal)
        
    def _assignFrom(self, source):
        source = toHVal(source)
        a = Assignment(source, self.next)
        a.cond = set()
        self.next.drivers.append(a)
        if not isinstance(source, Value):
            source.endpoints.append(a)
             
        return a


def areSameSignals(a, b):
    if a is b:
        return True
    if type(a) != type(b):
        return False 
    if len(a.drivers) != 1 or len(b.drivers) != 1:
        return False
    da = list(a.drivers)[0]
    db = list(b.drivers)[0]
    return da == db
