from typing import Set, Dict, Generator

from hwt.doc_markers import internal
from hwt.hdl.assignment import Assignment
from hwt.hdl.operator import Operator
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.statement import HdlStatement
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import SignalDriverErrType,\
    SignalDriverErr
from ipCorePackager.constants import DIRECTION


@internal
def walk_assignments(stm: HdlStatement, dst: RtlSignal)\
        -> Generator[Assignment, None, None]:
    if isinstance(stm, Assignment):
        if dst is stm.dst:
            yield stm
    else:
        for _stm in stm._iter_stms():
            yield from walk_assignments(_stm, dst)


@internal
def markVisibilityOfSignalsAndCheckDrivers(
        signals: Set[RtlSignal],
        interfaceSignals: Dict[RtlSignal, DIRECTION]):
    """
    * check if all signals are driven by something
    * mark signals with hidden = False if they are connecting statements
      or if they are external interface
    """
    signals_with_driver_issue = []
    for sig in signals:
        if isinstance(sig._nop_val, (RtlSignal, InterfaceBase)):
            sig._nop_val.hidden = False

        driver_cnt = len(sig.drivers)
        has_comb_driver = False
        if driver_cnt > 1:
            sig.hidden = False
            for d in sig.drivers:
                if not isinstance(d, Operator):
                    sig.hidden = False

                is_comb_driver = False

                if isinstance(d, HdlPortItem):
                    is_comb_driver = True
                elif d._event_dependent_from_branch is None:
                    for a in walk_assignments(d, sig):
                        if not a.indexes\
                                and a._event_dependent_from_branch != 0:
                            is_comb_driver = True
                            break

                if has_comb_driver and is_comb_driver:
                    signals_with_driver_issue.append(
                        (SignalDriverErrType.MULTIPLE_COMB_DRIVERS, sig))

                has_comb_driver |= is_comb_driver
        elif driver_cnt == 1:
            if not isinstance(sig.drivers[0], Operator):
                sig.hidden = False
        else:
            sig.hidden = False
            if sig not in interfaceSignals.keys():
                if not sig.def_val._is_full_valid():
                    signals_with_driver_issue.append(
                        (SignalDriverErrType.MISSING_DRIVER, sig))
                sig._const = True

        # chec interface direction if required
        d = interfaceSignals.get(sig, None)
        if d is None:
            pass
        elif d is DIRECTION.IN:
            assert sig.drivers, sig
            if len(sig.drivers) != 1:
                signals_with_driver_issue.append(
                    (SignalDriverErrType.INPUT_WITH_DRIVER, sig))
        elif d is DIRECTION.OUT:
            if not sig.drivers:
                signals_with_driver_issue.append(
                    (SignalDriverErrType.OUTPUT_WITHOUT_DRIVER, sig))

    if signals_with_driver_issue:
        raise SignalDriverErr(signals_with_driver_issue)
