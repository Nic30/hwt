from hwt.hdlObjects.types.defs import INT, SLICE
from hwt.hdlObjects.types.slice import Slice
from hwt.hdlObjects.types.typeCast import toHVal
from hwt.hdlObjects.value import Value


def slice_to_SLICE(sliceVals, width):
    # convert python slice to SLICE hdl type
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