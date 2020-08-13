from typing import Tuple, Callable, Union

from pyMathBitPrecise.array3t import Array3t
from pyMathBitPrecise.bits3t import Bits3t
from pyMathBitPrecise.enum3t import Enum3t

from hwt.doc_markers import internal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.value import HValue
from hwt.simulator.rtlSimulator import BasicRtlSimulatorWithSignalRegisterMethods
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pyDigitalWaveTools.json.writer import JsonWriter
from pyDigitalWaveTools.vcd.common import VCD_SIG_TYPE
from pycocotb.basic_hdl_simulator.proxy import BasicRtlSimProxy
from pycocotb.basic_hdl_simulator.sim_utils import ValueUpdater, \
    ArrayValueUpdater
from pyDigitalWaveTools.json.value_format import JsonBitsFormatter,\
    JsonEnumFormatter, JsonArrayFormatter


class BasicRtlSimulatorJson(BasicRtlSimulatorWithSignalRegisterMethods):
    supported_type_classes = (Bits, HEnum, HArray, Bits3t, Enum3t, Array3t)

    @internal
    def get_trace_formatter(self, t: HdlType)\
            -> Tuple[str, int, Callable[[RtlSignalBase, HValue], str]]:
        """
        :return: (vcd type name, vcd width, formatter fn)
        """
        if isinstance(t, (Bits3t, Bits)):
            return (VCD_SIG_TYPE.WIRE, t.bit_length(), JsonBitsFormatter())
        elif isinstance(t, (Enum3t, HEnum)):
            return (VCD_SIG_TYPE.ENUM, 1, JsonEnumFormatter())
        elif isinstance(t, (HArray, Array3t)):
            dimensions = []
            while isinstance(t, (HArray, Array3t)):
                dimensions.append(t.size)
                t = t.element_t
            _, _, elm_format = self.get_trace_formatter(t)
            return (VCD_SIG_TYPE.ARRAY,
                    dimensions + [t.bit_length(), ],
                    JsonArrayFormatter(dimensions, elm_format))
        else:
            raise ValueError(t)

    def create_wave_writer(self, data):
        self.wave_writer = JsonWriter(data)

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
