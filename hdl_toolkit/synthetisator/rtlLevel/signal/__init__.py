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
from hdl_toolkit.synthetisator.rtlLevel.mainBases import RtlSignalBase
from hdl_toolkit.simulator.utils import valHasChanged


class UniqList(list):
    def append(self, obj):
        if obj in self:
            pass
        return list.append(self, obj)

class RtlSignal(RtlSignalBase, SignalItem, SignalOps):
    """
    more like net
    @ivar _usedOps: dictionary of used operators which can be reused
    @ivar endpoints: UniqList of operators and statements for which this signal is driver.
    @ivar drivers: UniqList of operators and statements which can drive this signal.
    @ivar negated: this value represents that the value of signal has opposite meaning
           [TODO] mv negated to Bits hdl type.
    @ivar hiden: means that this signal is part of expression and should not be rendered 
    @ivar processCrossing: means that this signal is crossing process boundary
    """
    def __init__(self, name, dtype, defaultVal=None):
        if name is None:
            name = "sig_" + str(id(self))
            self.hasGenericName = True 
       
        assert isinstance(dtype, HdlType)
        super().__init__(name, dtype, defaultVal)
        # set can not be used because hash of items are changign
        self.endpoints = UniqList()
        self.drivers = UniqList()
        self._usedOps = {}
        self.negated = False
        self.hidden = True
        self.processCrossing = False
    
    def simPropagateChanges(self):
        if valHasChanged(self):
            conf = self._simulator.config
            env = self._simulator.env
            self._oldVal = self._val
            for e in self.endpoints:
                if conf.logPropagation:
                    conf.logPropagation("%d: Signal.simPropagateChanges %s -> %s" % (env.now, self.name, str(e)))
                yield env.process(e.simPropagateChanges())
        
    def staticEval(self):
        # operator writes in self._val new value
        if self.drivers:
            for d in self.drivers:
                d.staticEval()
        else:
            if isinstance(self.defaultVal, RtlSignal):
                self._val = self.defaultVal._val
            else:
                if not self._val.vldMask:  # [TODO] find better way how to find out if was initialized
                    self._val = self.defaultVal
        
        if not isinstance(self._val, Value):
            raise SimException("Evaluation of signal returned not supported object (%s)" % (repr(self._val)))
        return self._val
    
    def simUpdateVal(self, newVal):
        """
        Method called by simulator to update new value for this object
        """
        
        if not isinstance(newVal, Value):
            raise SimException("new value is instance of %s it should be instance of value" % (str(newVal.__class__)))
        self._val = newVal
        try:
            env = self._simulator.env
        except AttributeError:
            raise SimNotInitialized("Singal %s does not contains reference to its simulator" % (str(self)))
        c = self._simulator.config
        if  c.log:
            c.logChange(env.now, self, newVal)
        
        yield env.process(self.simPropagateChanges())
     
    def singleDriver(self):
        """
        Returns a first driver if signal has only one driver.
        """
        if len(self.drivers) != 1:
            raise MultipleDriversExc()
        return list(self.drivers)[0]
            
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
