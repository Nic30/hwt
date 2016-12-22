from datetime import datetime
from pprint import pprint
import sys

from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.boolean import Boolean
from hwt.simulator.hdlSimConfig import HdlSimConfig
from hwt.simulator.vcdWritter import VcdWritter
from hwt.hdlObjects.types.enum import Enum


class VcdHdlSimConfig(HdlSimConfig):
    supported_type_classes = (Boolean, Bits, Enum)
    
    def __init__(self, dumpFile=sys.stdout):
        super().__init__()
        self.vcdWritter = VcdWritter(dumpFile) 
        self.logPropagation = False
        self.logApplyingValues = False        

        # unit :  signal | unit
        # signal : None
        self.registered = {}
    
    
    def logApplyingValues(self, simulator, values):
        pprint((simulator.now, values))
        
    def logPropagation(self, simulator, signal, process): 
        print("%d: Signal.simPropagateChanges %s -> %s" % 
                                        (simulator.now, signal.name, str(process.name))
        )
        
    def vcdRegisterUnit(self, unit):
        with self.vcdWritter.module(unit._name) as m:
            for se in unit._cntx.signals:
                if isinstance(se._dtype, self.supported_type_classes):
                    m.var(se)
                    
            for u in unit._units:
                self.vcdRegisterUnit(u)
   
    
    def _registerSignal(self, sig):
        self.registered[sig] = None
   
    def beforeSim(self, simulator, synthesisedUnit):
        """
        This method is called before first step of simulation.
        """
        self.vcdWritter.date(datetime.now())
        self.vcdWritter.timescale(1)

        self.vcdRegisterUnit(synthesisedUnit)
        self.vcdWritter.enddefinitions()
        
    def logChange(self, nowTime, sig, nextVal):
        """
        This method is called for every value change of any signal.
        """
        try:
            self.vcdWritter.change(nowTime, sig, nextVal)
        except KeyError:
            # not every signal has to be registered
            pass
