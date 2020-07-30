from hwt.doc_markers import internal


@internal
def tryReduceAnd(sig, val):
    """
    Return sig and val reduced by & operator or None
    if it is not possible to statically reduce expression
    """
    m = sig._dtype.all_mask()
    if val._is_full_valid():
        v = val.val
        if v == m:
            return sig
        elif v == 0:
            return val


@internal
def tryReduceOr(sig, val):
    """
    Return sig and val reduced by | operator or None
    if it is not possible to statically reduce expression
    """
    m = sig._dtype.all_mask()
    if not val.vld_mask:
        return val

    if val._is_full_valid():
        v = val.val
        if v == m:
            return val
        elif v == 0:
            return sig


@internal
def tryReduceXor(sig, val):
    """
    Return sig and val reduced by ^ operator or None
    if it is not possible to statically reduce expression
    """
    m = sig._dtype.all_mask()
    if not val.vld_mask:
        return val

    if val._is_full_valid():
        v = val.val
        if v == m:
            return ~sig
        elif v == 0:
            return sig
