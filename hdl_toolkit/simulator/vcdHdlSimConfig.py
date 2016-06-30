import sys
from hdl_toolkit.simulator.vcdWritter import VcdWritter
from hdl_toolkit.synthetisator.rtlLevel.mainBases import RtlSignalBase
from datetime import datetime
from hdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from hdl_toolkit.simulator.hdlSimConfig import HdlSimConfig
from hdl_toolkit.hdlObjects.types.boolean import Boolean
from hdl_toolkit.hdlObjects.types.bits import Bits

class VcdHdlSimConfig(HdlSimConfig):
    def __init__(self, dumpFile=sys.stdout):
        # rising faling duration
        self.risFalDur = 100
        # operator propagation
        self.opPropagDur = 1000
        self.log = True
        self.vcdWritter = VcdWritter(dumpFile) 
        
        #self.logPropagation = False
    
    
    def vcdRegisterUnit(self, unit_name, sublements):
        with self.vcdWritter.module(unit_name) as m:
            for se , ssitems in sublements.items():
                if isinstance(se, RtlSignalBase): 
                    if isinstance(se._dtype, (Boolean, Bits)):
                        m.var(se)
                else:
                    raise NotImplementedError(se)
   
    def beforeSim(self, simulator):
        """
        This method is called before first step of simulation.
        """
        
        topSigs = {}
        self.vcdWritter.date(datetime.now())
        self.vcdWritter.timescale(1)
        for k, v in simulator.registered.items():
            if isinstance(k, Unit):
                self.vcdRegisterUnit(k._name, v)
            else:
                topSigs[k] = None
        
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
            pass