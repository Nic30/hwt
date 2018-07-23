from datetime import datetime
import sys
from typing import Union, Optional, Tuple, Callable

from hwt.hdl.types.bits import Bits
from hwt.hdl.types.bool import HBool
from hwt.hdl.types.enum import HEnum
from hwt.hdl.value import Value
from hwt.simulator.hdlSimConfig import HdlSimConfig
from hwt.simulator.types.simBits import SimBitsT
from hwt.synthesizer.interface import Interface
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.unit import Unit
from pyDigitalWaveTools.vcd.common import VCD_SIG_TYPE
from pyDigitalWaveTools.vcd.writer import VcdWriter, VcdVarWritingScope, \
    vcdBitsFormatter, vcdEnumFormatter, VarAlreadyRegistered
from hwt.simulator.simModel import SimModel


def vcdTypeInfoForHType(t) -> Tuple[str, int, Callable[[RtlSignalBase, Value], str]]:
    """
    :return: (vcd type name, vcd width)
    """
    if isinstance(t, (SimBitsT, Bits, HBool)):
        return (VCD_SIG_TYPE.WIRE, t.bit_length(), vcdBitsFormatter)
    elif isinstance(t, HEnum):
        return (VCD_SIG_TYPE.REAL, 1, vcdEnumFormatter)
    else:
        raise ValueError(t)


class VcdHdlSimConfig(HdlSimConfig):
    supported_type_classes = (HBool, Bits, HEnum)

    def __init__(self, dumpFile=sys.stdout):
        self.vcdWriter = VcdWriter(dumpFile)
        self.logPropagation = False
        self.logApplyingValues = False
        self._obj2scope = {}

    def vcdRegisterInterfaces(self, obj: Union[Interface, Unit],
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
                    self.vcdRegisterInterfaces(chIntf, subScope)

                if isinstance(obj, (Unit, SimModel)):
                    # register interfaces from all subunits
                    for u in obj._units:
                        self.vcdRegisterInterfaces(u, subScope)

            return subScope
        else:
            t = obj._dtype
            if isinstance(t, self.supported_type_classes):
                tName, width, formatter = vcdTypeInfoForHType(t)
                try:
                    parent.addVar(obj, getSignalName(obj), tName, width, formatter)
                except VarAlreadyRegistered:
                    pass

    def vcdRegisterRemainingSignals(self, unit: Union[Interface, Unit]):
        unitScope = self._obj2scope[unit]
        for s in unit._ctx.signals:
            if s not in self.vcdWriter._idScope:
                t = s._dtype
                if isinstance(t, self.supported_type_classes):
                    tName, width, formatter = vcdTypeInfoForHType(t)
                    unitScope.addVar(s, getSignalName(
                        s), tName, width, formatter)

        for u in unit._units:
            self.vcdRegisterRemainingSignals(u)

    def initUnitSignalsForInterfaces(self, unit):
        self._scope = self.registerInterfaces(unit)
        for s in unit._ctx.signals:
            if s not in self.vcdWriter._idScope:
                self.registerSignal(s)

        for u in unit._units:
            self.initUnitSignals(u)

    def beforeSim(self, simulator, synthesisedUnit):
        """
        This method is called before first step of simulation.
        """
        vcd = self.vcdWriter
        vcd.date(datetime.now())
        vcd.timescale(1)

        self.vcdRegisterInterfaces(synthesisedUnit, None)
        self.vcdRegisterRemainingSignals(synthesisedUnit)

        vcd.enddefinitions()

    def logChange(self, nowTime, sig, nextVal):
        """
        This method is called for every value change of any signal.
        """
        try:
            self.vcdWriter.logChange(nowTime, sig, nextVal)
        except KeyError:
            # not every signal has to be registered
            pass
