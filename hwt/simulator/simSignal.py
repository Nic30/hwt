from hwt.hdl.variables import SignalItem


class SimSignal(SignalItem):
    """
    Class of signal simulation functions

    :ivar _writeCallbacks: list of callback functions(signal, simulator)
        which is called when new (changed) value is written to this signal
    """
    __slots__ = ["name", "_val", "_oldVal", "_writeCallbacks",
                 "simSensProcs", "simRisingSensProcs", "simFallingSensProcs"]

    def __init__(self, ctx, name, dtype, defaultVal=None):
        ctx.signals.add(self)
        self.hidden = False
        self._writeCallbacks = []
        self._writeCallbacksToEn = []
        self.simSensProcs = set()
        self.simRisingSensProcs = set()
        self.simFallingSensProcs = set()
        super(SimSignal, self).__init__(name, dtype, defaultVal)

    def registerWriteCallback(self, callback, getEnFn) -> int:
        """
        Register writeCallback for signal.
        Registration is evaluated at the end of deltastep of simulator.

        :param callback: simulation process represented by function(simulator)
            which should be called after update of this signal
        :param getEnFn: function() to get initial value for enable of callback
        """
        index = len(self._writeCallbacks)
        self._writeCallbacks.append(None)
        self._writeCallbacksToEn.append((index, callback, getEnFn))
        return index

    def _loadWriteCallbacks(self):
        wc = self._writeCallbacksToEn
        self._writeCallbacksToEn = []
        # perform registration of new write callbacks
        for i, callback, reqEnFn in wc:
            if reqEnFn():
                self._writeCallbacks[i] = callback

    def simPropagateChanges(self, simulator):
        v = self._val
        self._oldVal = v

        if self._writeCallbacksToEn:
            self._loadWriteCallbacks()
        # run all sensitive processes
        log = simulator.config.logPropagation
        if log:
            log(simulator, self, self.simSensProcs)
        for p in self.simSensProcs:
            simulator.addHwProcToRun(self, p)

        # run write callbacks we have to create new list to allow
        # registering of new call backs in callbacks
        for c in self._writeCallbacks:
            if c:
                # run simulation processes which are activated
                simulator.process(c(simulator))

        if self.simRisingSensProcs:
            if v.val or not v.vldMask:
                if log:
                    log(simulator, self, self.simRisingSensProcs)
                for p in self.simRisingSensProcs:

                    simulator.addHwProcToRun(self, p)

        if self.simFallingSensProcs:
            if not v.val or not v.vldMask:
                if log:
                    log(simulator, self, self.simFallingSensProcs)
                for p in self.simFallingSensProcs:
                    simulator.addHwProcToRun(self, p)

    def simUpdateVal(self, simulator, valUpdater):
        """
        Method called by simulator to update new value for this object
        """
        dirtyFlag, newVal = valUpdater(self._oldVal)

        if dirtyFlag:
            self._val = newVal
            newVal.updateTime = simulator.now
            log = simulator.config.logChange
            if log:
                log(simulator.now, self, newVal)

            self.simPropagateChanges(simulator)

    def __repr__(self):
        return "<%s, %s>" % (self.__class__.__name__, self.name)
