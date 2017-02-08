from hwt.hdlObjects.variables import SignalItem

class SimSignal(SignalItem):
    """
    Class of signal simulation functions
    
    @ivar _writeCallbacks: list of callback functions(signal, simulator) which is called
                           when new (changed) value is written to this signal
    """
    __slots__ = ["name", "_val", "_oldVal", "_writeCallbacks",
                 "simSensProcs", "simRisingSensProcs", "simFallingSensProcs"]
    def __init__(self, ctx, name, dtype, defaultVal=None):
        ctx.signals.add(self)
        self.hidden = False
        self._writeCallbacks = []
        self.simSensProcs = set()
        self.simRisingSensProcs = set()
        self.simFallingSensProcs = set()
        super(SimSignal, self).__init__(name, dtype, defaultVal)
        
    
    def simPropagateChanges(self, simulator):
        v = self._val
        self._oldVal = v

        # run all sensitive processes    
        log = simulator.config.logPropagation
        for p in self.simSensProcs:        
            if log:
                log(simulator, self, p)
                
            simulator.addHwProcToRun(self, p)

        if self.simRisingSensProcs or self.simFallingSensProcs: 
            if v.val or not v.vldMask:
                for p in self.simRisingSensProcs:        
                    if log:
                        log(simulator, self, p)
                
                    simulator.addHwProcToRun(self, p)
                    
            if not v.val or not v.vldMask:
                for p in self.simFallingSensProcs:        
                    if log:
                        log(simulator, self, p)
                
                    simulator.addHwProcToRun(self, p)
    
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
            # registering of new call backs in callbacks
            callBacks = self._writeCallbacks
            self._writeCallbacks = []
            for c in callBacks:
                # simulation processes
                simulator.process(c(simulator))

            self.simPropagateChanges(simulator)
