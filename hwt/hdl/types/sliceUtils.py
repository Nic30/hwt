from hwt.hdl.types.defs import INT, SLICE
from hwt.hdl.types.slice import Slice
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import Value
from hwt.doc_markers import internal


@internal
def slice_to_SLICE(sliceVals, width):
    """convert python slice to value of SLICE hdl type"""
    if sliceVals.step is not None:
        raise NotImplementedError()

    start = sliceVals.start
    stop = sliceVals.stop

    if sliceVals.start is None:
        start = INT.fromPy(width)
    else:
        start = toHVal(sliceVals.start)

    if sliceVals.stop is None:
        stop = INT.fromPy(0)
    else:
        stop = toHVal(sliceVals.stop)

    startIsVal = isinstance(start, Value)
    stopIsVal = isinstance(stop, Value)

    indexesAreValues = startIsVal and stopIsVal
    if indexesAreValues:
        updateTime = max(start.updateTime, stop.updateTime)
    else:
        updateTime = -1

    return Slice.getValueCls()((start, stop), SLICE, 1, updateTime)
