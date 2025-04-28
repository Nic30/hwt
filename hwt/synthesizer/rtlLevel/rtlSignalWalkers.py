from hwt.doc_markers import internal
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import isEventDependentOp
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.mainBases import RtlSignalBase


@internal
def discoverEventDependency(sig: RtlSignalBase):
    """
    :return: generator of tuples (event operator, signal)
    """

    try:
        drivers = sig._rtlDrivers
    except AttributeError:
        return

    if len(drivers) == 1:
        d = drivers[0]
        if isinstance(d, HOperatorNode):
            if isEventDependentOp(d.operator):
                yield (d.operator, d.operands[0])
            else:
                for op in d.operands:
                    yield from discoverEventDependency(op)


@internal
def discover_sensitivity_of_sig(signal: RtlSignalBase,
                              seen: set, ctx: SensitivityCtx):
    casualSensitivity = set()
    signal._walk_sensitivity(casualSensitivity, seen, ctx)
    if not ctx.contains_ev_dependency:
        # if event dependent sensitivity found do not add other sensitivity
        ctx.extend(casualSensitivity)
