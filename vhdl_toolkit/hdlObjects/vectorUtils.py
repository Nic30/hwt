from vhdl_toolkit.hdlObjects.operatorDefs import AllOps
from vhdl_toolkit.hdlObjects.typeDefs import Integer


def getWidthExpr(vectorTypeInst):
    downto = vectorTypeInst.constrain.singleDriver()
    
    assert(downto.operator == AllOps.DOWNTO)
    assert(downto.ops[1].val == 0)
    
    
    widthMinOne = downto.ops[0]
    if isinstance(widthMinOne, Integer.ValueCls):
        w = widthMinOne.clone()
        w.val += 1
        return w
    else:
        widthMinOne = widthMinOne.singleDriver()
    assert(widthMinOne.operator == AllOps.MINUS)
    assert(widthMinOne.ops[1].val == 1)
    
    return widthMinOne.ops[0]
