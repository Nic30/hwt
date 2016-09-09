from datetime import datetime
from pprint import pprint
import sys

from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.boolean import Boolean
from hdl_toolkit.simulator.hdlSimConfig import HdlSimConfig
from hdl_toolkit.simulator.vcdWritter import VcdWritter


class VcdHdlSimConfig(HdlSimConfig):
    supported_type_classes = (Boolean, Bits)
    
    def __init__(self, dumpFile=sys.stdout):
        super().__init__()
        self.vcdWritter = VcdWritter(dumpFile) 
        self.logPropagation = False
        self.logApplyingValues = False        

        # unit :  signal | unit
        # signal : None
        self.registered = {}
    
    
    def logApplyingValues(self, simulator, values):
        pprint((simulator.env.now, values))
        
    def logPropagation(self, simulator, signal, process): 
        print("%d: Signal.simPropagateChanges %s -> %s" % 
                                        (simulator.env.now, signal.name, str(process.name))
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
