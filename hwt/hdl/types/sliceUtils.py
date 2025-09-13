from hwt.doc_markers import internal
from hwt.hdl.types.defs import INT, SLICE
from hwt.hdl.types.slice import HSlice
from hwt.hdl.types.typeCast import toHVal


@internal
def slice_to_HSlice(sliceVals: slice, widthOfSlicedVec: int):
    """convert python slice to value of SLICE hdl type"""
    if sliceVals.step is None:
        step = -1
    else:
        step = sliceVals.step

    start = sliceVals.start
    if start is None:
        start = INT.from_py(widthOfSlicedVec)
    else:
        start = toHVal(start)

    stop = sliceVals.stop
    if stop is None:
        stop = INT.from_py(0)
    else:
        stop = toHVal(stop)

    v = slice(start, stop, step)
    return HSlice.getConstCls()(SLICE, v, 1)
