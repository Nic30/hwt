from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.types.defs import Integer
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.types.sliceVal import SliceVal


def getWidthExpr(vectorTypeInst):
    c = vectorTypeInst.constrain
    if isinstance(c, SliceVal):
        return c.val[0] + 1
    downto = c.singleDriver()
    
    assert downto.operator == AllOps.DOWNTO
    assert downto.ops[1].val == 0
    
    
    widthMinOne = downto.ops[0]
    if isinstance(widthMinOne, Value) and isinstance(widthMinOne._dtype, Integer):
        w = widthMinOne.clone()
        w.val += 1
        return w
    else:
        widthMinOne = widthMinOne.singleDriver()
    assert widthMinOne.operator == AllOps.SUB
    assert widthMinOne.ops[1].val == 1
    
    return widthMinOne.ops[0]
