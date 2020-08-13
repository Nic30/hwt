
import sys

from pyMathBitPrecise.bits3t import Bits3t
from pyMathBitPrecise.enum3t import Enum3t

from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.simulator.rtlSimulator import BasicRtlSimulatorWithSignalRegisterMethods
from pyDigitalWaveTools.vcd.writer import VcdWriter
from pycocotb.basic_hdl_simulator.proxy import BasicRtlSimProxy
from hwt.hdl.value import HValue
from typing import Union
from pycocotb.basic_hdl_simulator.sim_utils import ValueUpdater,\
    ArrayValueUpdater


class BasicRtlSimulatorVcd(BasicRtlSimulatorWithSignalRegisterMethods):
    supported_type_classes = (Bits, HEnum, Bits3t, Enum3t)

    def create_wave_writer(self, file_name):
        self.wave_writer = VcdWriter(open(file_name, "w"))

    def finalize(self):
        # because set_trace_file() may not be called
        # and it this case the vcd config is not set
        f = self.wave_writer._oFile
        if f not in (sys.__stderr__, sys.__stdin__, sys.__stdout__):
            f.close()

    def logChange(self, nowTime: int,
                  sig: BasicRtlSimProxy, 
                  nextVal: HValue,
                  valueUpdater: Union[ValueUpdater, ArrayValueUpdater]):
        """
        This method is called for every value change of any signal.
        """
        try:
            self.wave_writer.logChange(nowTime, sig, nextVal, valueUpdater)
        except KeyError:
            # not every signal has to be registered
            # (if it is not registered it means it is ignored)
            pass
