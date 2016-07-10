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
from hdl_toolkit.hdlObjects.portItem import PortItem


def hasDiferentVal(reference, sigOrVal):
    assert isinstance(reference, Value)
    if isinstance(sigOrVal, Value):
        v = sigOrVal
    else:
        v = sigOrVal._val
    
    return reference != v

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
        
        self.simSensitiveProcesses = set()
    
    def simPropagateChanges(self, simulator):
        if valHasChanged(self):
            self._oldVal = self._val

            for e in self.endpoints:
                if isinstance(e, PortItem):
                    si = e.portItem._interface._sigInside
                    if self is si:
                        # OUT port
                        raise NotImplementedError()
                    else:
                        # IN port
                        si.simUpdateVal(simulator, self._val)
                else:
                    try:
                        isIndexOnMe = e.op == AllOps.INDEX and e.result != self
                    except AttributeError:
                        isIndexOnMe = False
                    
                    if isIndexOnMe:
                        # if i has index which I am driver for
                        raise NotImplementedError()
                
            conf = simulator.config
            for p in self.simSensitiveProcesses:        
                if conf.logPropagation:
                    conf.logPropagation("%d: Signal.simPropagateChanges %s -> %s" % 
                                        (simulator.env.now, self.name, str(p.name)))
                simulator.addHwProcToRun(p)
        
    def staticEval(self):
        # operator writes in self._val new value
        if self.drivers:
            for d in self.drivers:
                d.staticEval()
        else:
            if isinstance(self.defaultVal, RtlSignal):
                self._val = self.defaultVal._val
            else:
                # [TODO] find better way how to find out if was initialized
                if not self._val.vldMask:  
                    self._val = self.defaultVal
        
        if not isinstance(self._val, Value):
            raise SimException("Evaluation of signal returned not supported object (%s)" % (repr(self._val)))
        return self._val
    
    def simEval(self, simulator):
        """
        Evaluate, signals which have hidden flag set
        @attention: single process has to drive single variable in order to work
        """
        for d in self.drivers:
            if not isinstance(d, Assignment):
                d.simEval(simulator)
        if not isinstance(self._val, Value):
            raise SimException("Evaluation of signal returned not supported object (%s)" % (repr(self._val)))
        return self._val
        
    
    def simUpdateVal(self, simulator, newVal):
        """
        Method called by simulator to update new value for this object
        """
        
        if not isinstance(newVal, Value):
            raise SimException("new value is instance of %s it should be instance of value" % (str(newVal.__class__)))
        self._val = newVal
        
        c = simulator.config
        if  c.logChange:
            c.logChange(simulator.env.now, self, newVal)
        
        self.simPropagateChanges(simulator)
     
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
