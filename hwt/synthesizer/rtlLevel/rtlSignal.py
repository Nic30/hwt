from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.value import Value
from hwt.hdlObjects.variables import SignalItem
from hwt.simulator.exceptions import SimException
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hwt.synthesizer.rtlLevel.signalUtils.ops import RtlSignalOps
from hwt.synthesizer.uniqList import UniqList


class RtlSignal(RtlSignalBase, SignalItem, RtlSignalOps):
    """
    more like net
    @ivar _usedOps: dictionary of used operators which can be reused
    @ivar endpoints: UniqList of operators and statements for which this signal is driver.
    @ivar drivers: UniqList of operators and statements which can drive this signal.
    @ivar negated: this value represents that the value of signal has opposite meaning
           [TODO] mv negated to Bits hdl type.
    @ivar hiden: means that this signal is part of expression and should not be rendered 
    @ivar processCrossing: means that this signal is crossing process boundary
    
    @cvar __instCntr: counter used for generating instance ids
    @ivar _instId: internaly used only for intuitive sorting of statements
    """
    __instCntr = 0

    def __init__(self, ctx, name, dtype, defaultVal=None, nopVal=None, useNopVal=False):
        """
        @param ctx: context - RtlNetlist which is this signal part of
        @param name: name hint for this signal, if is None name is choosen automaticaly
        @param defaultVal: value which is used for reset and as default value in hdl
        @param useNopVal: use nopVal or ignore it
        @param nopVal: value which is used to fill up statements when no other value is assigned
        """
        
        if name is None:
            name = "sig_"
            self.hasGenericName = True
        else:
            self.hasGenericName = False  
       
        assert isinstance(dtype, HdlType)
        super(RtlSignal, self).__init__(name, dtype, defaultVal)
        self.ctx = ctx
        
        if ctx: 
            # params does not have any signal on created and it is assigned after param is bounded to unit
            ctx.signals.add(self)
            
        # set can not be used because hash of items are changign
        self.endpoints = UniqList()
        self.drivers = UniqList()
        self._usedOps = {}
        self.negated = False
        self.hidden = True
        self._instId = RtlSignal._nextInstId()
        
        self._nopVal = nopVal
        self._useNopVal = useNopVal 

    
    @classmethod
    def _nextInstId(cls):
        """
        Get next instance id
        """
        i = cls.__instCntr
        cls.__instCntr += 1
        return i
    
    def staticEval(self):
        # operator writes in self._val new value
        if self.drivers:
            for d in self.drivers:
                d.staticEval()
        else:
            if isinstance(self.defaultVal, RtlSignal):
                self._val = self.defaultVal._val.staticEval()
            else:
                if self._val.updateTime < 0:  
                    self._val = self.defaultVal.clone()
        
        if not isinstance(self._val, Value):
            raise SimException("Evaluation of signal returned not supported object (%s)" % 
                               (repr(self._val)))
        return self._val
    
      
    def singleDriver(self):
        """
        Returns a first driver if signal has only one driver.
        """
        if len(self.drivers) != 1:
            raise MultipleDriversExc()
        return list(self.drivers)[0]

