from hwt.doc_markers import internal
from hwt.hdl.types.defs import INT, SLICE
from hwt.hdl.types.slice import Slice
from hwt.hdl.types.typeCast import toHVal


@internal
def slice_to_SLICE(sliceVals, width):
    """convert python slice to value of SLICE hdl type"""
    if sliceVals.step is None:
        step = -1
    else:
        step = sliceVals.step

    start = sliceVals.start
    if start is None:
        start = INT.from_py(width)
    else:
        start = toHVal(start)

    stop = sliceVals.stop
    if stop is None:
        stop = INT.from_py(0)
    else:
        stop = toHVal(stop)

    v = slice(start, stop, step)
    return Slice.getValueCls()(SLICE, v, 1)
