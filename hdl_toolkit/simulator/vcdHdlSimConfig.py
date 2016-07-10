import sys
from hdl_toolkit.simulator.vcdWritter import VcdWritter
from hdl_toolkit.synthetisator.rtlLevel.mainBases import RtlSignalBase
from datetime import datetime
from hdl_toolkit.simulator.hdlSimConfig import HdlSimConfig
from hdl_toolkit.hdlObjects.types.boolean import Boolean
from hdl_toolkit.hdlObjects.types.bits import Bits

class VcdHdlSimConfig(HdlSimConfig):
    supported_type_classes = (Boolean,  Bits)
    
    def __init__(self, dumpFile=sys.stdout):
        super().__init__()
        self.vcdWritter = VcdWritter(dumpFile) 
        self.logPropagation = False
        
        # unit :  signal | unit
        # signal : None
        self.registered = {}
    
    
    def vcdRegisterUnit(self, unit_name, sublements):
        with self.vcdWritter.module(unit_name) as m:
            for se , ssitems in sublements.items():
                if isinstance(se, RtlSignalBase): 
                    if isinstance(se._dtype, self.supported_type_classes):
                        m.var(se)
                else:
                    raise NotImplementedError(se)
   
    
    def _registerSignal(self, sig):
        self.registered[sig] = None
   
    def beforeSim(self, simulator, signals):
        """
        This method is called before first step of simulation.
        """
        
        topSigs = {}
        self.vcdWritter.date(datetime.now())
        self.vcdWritter.timescale(1)
        for s in signals:
            topSigs[s] = None
        
        if topSigs:
            self.vcdRegisterUnit("top", topSigs)
        self.vcdWritter.enddefinitions()
        
    def logChange(self, nowTime, sig, nextVal):
        """
        This method is called for every value change of any signal.
        """
        try:
            self.vcdWritter.change(nowTime, sig, nextVal)
        except KeyError:
            # signal is not registered
            pass
