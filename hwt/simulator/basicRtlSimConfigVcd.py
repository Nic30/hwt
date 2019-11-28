from datetime import datetime
import sys
from typing import Union, Optional, Tuple, Callable

from hwt.doc_markers import internal
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.value import Value
from hwt.synthesizer.interface import Interface
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.unit import Unit
from pyDigitalWaveTools.vcd.common import VCD_SIG_TYPE
from pyDigitalWaveTools.vcd.writer import VcdWriter, VcdVarWritingScope, \
    vcdBitsFormatter, vcdEnumFormatter, VarAlreadyRegistered
from pycocotb.basic_hdl_simulator.config import BasicRtlSimConfig
from pycocotb.basic_hdl_simulator.model import BasicRtlSimModel
from pycocotb.basic_hdl_simulator.proxy import BasicRtlSimProxy
from pycocotb.hdlSimulator import HdlSimulator
from pyMathBitPrecise.bits3t import Bits3t
from pyMathBitPrecise.enum3t import Enum3t


@internal
def vcdTypeInfoForHType(t)\
        ->Tuple[str, int, Callable[[RtlSignalBase, Value], str]]:
    """
    :return: (vcd type name, vcd width)
    """
    if isinstance(t, (Bits3t, Bits)):
        return (VCD_SIG_TYPE.WIRE, t.bit_length(), vcdBitsFormatter)
    elif isinstance(t, (Enum3t, HEnum)):
        return (VCD_SIG_TYPE.REAL, 1, vcdEnumFormatter)
    else:
        raise ValueError(t)


class BasicRtlSimConfigVcd(BasicRtlSimConfig):
    supported_type_classes = (Bits, HEnum, Bits3t, Enum3t)

    def __init__(self, dumpFile=sys.stdout):
        self.vcdWriter = VcdWriter(dumpFile)
        self.logPropagation = False
        self.logApplyingValues = False
        self._obj2scope = {}
        self._traced_signals = set()

    def vcdRegisterInterfaces(self,
            obj: Union[Interface, Unit],
            model: BasicRtlSimModel,
            parent: Optional[VcdVarWritingScope]):
        """
        Register signals from interfaces for Interface or Unit instances
        """
        if hasattr(obj, "_interfaces") and obj._interfaces:
            name = obj._name
            parent_ = self.vcdWriter if parent is None else parent

            subScope = parent_.varScope(name)
            self._obj2scope[obj] = subScope

            with subScope:
                # register all subinterfaces
                for chIntf in obj._interfaces:
                    self.vcdRegisterInterfaces(chIntf, model, subScope)

                if isinstance(obj, Unit):
                    # register interfaces from all subunits
                    for u in obj._units:
                        m = getattr(model, u._name + "_inst")
                        self.vcdRegisterInterfaces(u, m, subScope)

            return subScope
        else:
            t = obj._dtype
            if isinstance(t, self.supported_type_classes):
                tName, width, formatter = vcdTypeInfoForHType(t)
                sig_name = obj._sigInside.name
                s = getattr(model.io, sig_name)
                try:
                    parent.addVar(s, sig_name,
                                  tName, width, formatter)
                except VarAlreadyRegistered:
                    pass

    def vcdRegisterRemainingSignals(self, unit: Union[Interface, Unit],
                                    model: BasicRtlSimModel):
        unitScope = self._obj2scope[unit]
        # for s in unit._ctx.signals:
        #    if not s.hidden and s not in self.vcdWriter._idScope:
        #        t = s._dtype
        #        if isinstance(t, self.supported_type_classes):
        #            tName, width, formatter = vcdTypeInfoForHType(t)
        #            unitScope.addVar(s, getSignalName(
        #                s), tName, width, formatter)
        #
        for s in model._interfaces:
            if s not in self.vcdWriter._idScope:
                t = s._dtype
                if isinstance(t, self.supported_type_classes):
                    tName, width, formatter = vcdTypeInfoForHType(t)
                    try:
                        unitScope.addVar(s, s._name, tName, width, formatter)
                    except VarAlreadyRegistered:
                        pass
        for u in unit._units:
            m = getattr(model, u._name + "_inst")
            self.vcdRegisterRemainingSignals(u, m)

    def beforeSim(self, simulator: HdlSimulator,
                  synthesisedUnit: Unit, model: BasicRtlSimModel):
        """
        This method is called before first step of simulation.
        """
        vcd = self.vcdWriter
        vcd.date(datetime.now())
        vcd.timescale(1)

        self.vcdRegisterInterfaces(synthesisedUnit, model, None)
        self.vcdRegisterRemainingSignals(synthesisedUnit, model)

        vcd.enddefinitions()

    def logChange(self, nowTime: int, sig: BasicRtlSimProxy, nextVal):
        """
        This method is called for every value change of any signal.
        """
        try:
            self.vcdWriter.logChange(nowTime, sig, nextVal)
        except KeyError:
            # not every signal has to be registered
            # (if it is not registered it means it is ignored)
            pass
