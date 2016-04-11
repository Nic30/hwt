from vhdl_toolkit.hdlObjects.operatorDefs import AllOps

def getWidthExpr(vectorTypeInst):
    downto = vectorTypeInst.constrain.singleDriver()
    
    assert(downto.operator == AllOps.DOWNTO)
    assert(downto.ops[1].val == 0)
    
    widthMinOne = downto.ops[0].singleDriver()
    
    assert(widthMinOne.operator == AllOps.MINUS)
    assert(widthMinOne.ops[1].val == 1)
    
    return widthMinOne.ops[0]