

def internal(fn):
    """
    Decorator which does not affect functionality but it is used as marker
    which tells that this object is not interesting for users and it is only used internally 
    """
    return fn

def hwt_expr_producer(fn):
    """
    Decorator which does not affect functionality.
    For documentation purposes it specifies that the function produces hwt expression.
    """
    return fn