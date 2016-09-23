from hdl_toolkit.hdlObjects.assignment import Assignment
from hdl_toolkit.hdlObjects.portItem import PortItem
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.simulator.exceptions import SimException


class SimSignal():
    """
    Class of signal simulation functions
    
    @ivar _writeCallbacks: list of callback functions(signal, simulator) which is called
                           when new (changed) value is written to this signal
    """

    def __init__(self):
        self._writeCallbacks = []
        self.simSensitiveProcesses = set()
    
    def simPropagateChanges(self, simulator):
        self._oldVal = self._val

        for e in self.endpoints:
            if isinstance(e, PortItem) and e.dst is not None:
                e.dst.simUpdateVal(simulator, lambda v: (True, self._val))
            
        log = simulator.config.logPropagation
        for p in self.simSensitiveProcesses:        
            if log:
                log(simulator, self, p)
                
            simulator.addHwProcToRun(p)

    def simEval(self, simulator):
        """
        Evaluate, signals which have hidden flag set
        @attention: single process has to drive single variable in order to work
        """
        for d in self.drivers:
            if isinstance(d, Assignment):
                continue
            
            d.simEval(simulator)
            
        if not isinstance(self._val, Value):
            raise SimException("Evaluation of signal returned not supported object (%s)" % 
                               (repr(self._val)))
        return self._val
    
    def simUpdateVal(self, simulator, valUpdater):
        """
        Method called by simulator to update new value for this object
        """
        
        dirtyFlag, newVal = valUpdater(self._oldVal)
        self._val = newVal
        newVal.updateTime = simulator.now
        
        if dirtyFlag:
            log = simulator.config.logChange
            if  log:
                log(simulator.now, self, newVal)
            
            # run write callbacks we have to create new list to allow 
            # registerring of new call backs in callbacks
            callBacks = self._writeCallbacks
            self._writeCallbacks = []
            for c in callBacks:
                # simulation processes
                simulator.process(c(simulator))

            self.simPropagateChanges(simulator)
