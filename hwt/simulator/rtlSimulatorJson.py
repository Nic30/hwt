from typing import Tuple, Callable, Union

from pyMathBitPrecise.array3t import Array3t
from pyMathBitPrecise.bits3t import Bits3t
from pyMathBitPrecise.enum3t import Enum3t

from hwt.doc_markers import internal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.value import Value
from hwt.simulator.rtlSimulator import BasicRtlSimulatorWithSignalRegisterMethods
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pyDigitalWaveTools.json.writer import JsonWriter, jsonBitsFormatter, \
    jsonEnumFormatter
from pyDigitalWaveTools.vcd.common import VCD_SIG_TYPE
from pycocotb.basic_hdl_simulator.proxy import BasicRtlSimProxy
from pycocotb.basic_hdl_simulator.sim_utils import ValueUpdater, \
    ArrayValueUpdater


class BasicRtlSimulatorJson(BasicRtlSimulatorWithSignalRegisterMethods):
    supported_type_classes = (Bits, HEnum, HArray, Bits3t, Enum3t, Array3t)

    @internal
    def get_trace_formater(self, t: HdlType)\
            -> Tuple[str, int, Callable[[RtlSignalBase, Value], str]]:
        """
        :return: (vcd type name, vcd width, formater fn)
        """
        if isinstance(t, (Bits3t, Bits)):
            return (VCD_SIG_TYPE.WIRE, t.bit_length(), jsonBitsFormatter)
        elif isinstance(t, (Enum3t, HEnum)):
            return (VCD_SIG_TYPE.REAL, 1, jsonEnumFormatter)
        elif isinstance(t, (HArray, Array3t)):
            return (VCD_SIG_TYPE.ARRAY, t.size, self.get_trace_formater(t.element_t))
        else:
            raise ValueError(t)

    def create_wave_writer(self, data):
        self.wave_writer = JsonWriter(data)

    def logChange(self, nowTime: int,
                  sig: BasicRtlSimProxy, 
                  nextVal: Value,
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
