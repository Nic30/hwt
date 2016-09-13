def vldMaskForAnd(a, b):
    # (val, vld)
    # (0, 0) & (0, 0) -> (0, 0) 
    # (0, 1) & (0, 0) -> (0, 1)
    # (0, 0) & (0, 1) -> (0, 1)
    # (1, 1) & (0, 0) -> (0, 0)
    
    a_vld = (a.vldMask & ~a.val)
    b_vld = (b.vldMask & ~b.val)
    vld = (a.vldMask & b.vldMask) | a_vld | b_vld
    return vld  

def vldMaskForOr(a, b):
    a_vld = (a.vldMask & a.val)
    b_vld = (b.vldMask & b.val)
    vld = (a.vldMask & b.vldMask) | a_vld | b_vld
    return vld  

def vldMaskForXor(a, b):
    return a.vldMask & b.vldMask