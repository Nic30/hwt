from typing import Generator, Tuple, List

from hwt.doc_markers import internal
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.statement import HdlStatement
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErrType, \
    SignalDriverErr
from hwt.synthesizer.rtlLevel.rtlNetlistPass import RtlNetlistPass
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from ipCorePackager.constants import DIRECTION


@internal
def walk_assignments(stm: HdlStatement, dst: RtlSignal)\
        ->Generator[HdlAssignmentContainer, None, None]:
    if isinstance(stm, HdlAssignmentContainer):
        if dst is stm.dst:
            yield stm
    else:
        for _stm in stm._iter_stms():
            yield from walk_assignments(_stm, dst)


@internal
class RtlNetlistPassMarkVisibilityOfSignalsAndCheckDrivers(RtlNetlistPass):

    def runOnRtlNetlist(self, netlist: "RtlNetlist"):
        """
        * check if all signals are driven by something
        * mark signals with hidden = False if they are connecting statements
          or if they are external interface
        """
        signals = netlist.signals
        ioSignals = netlist.hwIOs

        signals_with_driver_issue: List[Tuple[SignalDriverErrType, RtlSignal]] = []
        for sig in signals:
            # if isinstance(sig._nop_val, (RtlSignal, InterfaceBase)):
            #    sig._nop_val.hidden = False

            driver_cnt = len(sig.drivers)
            has_comb_driver = False
            if driver_cnt > 1:
                sig.hidden = False
                for d in sig.drivers:
                    if not isinstance(d, HOperatorNode):
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
                        break

                    has_comb_driver |= is_comb_driver
            elif driver_cnt == 1:
                if not isinstance(sig.drivers[0], HOperatorNode):
                    sig.hidden = False
            else:
                sig.hidden = False
                if sig not in ioSignals.keys():
                    if not sig.def_val._is_partially_valid():
                        signals_with_driver_issue.append(
                            (SignalDriverErrType.MISSING_DRIVER, sig))
                    sig._const = True

            # chec interface direction if required
            d = ioSignals.get(sig, None)
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
