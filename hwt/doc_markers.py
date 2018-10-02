

def internal(fn):
    """
    Decorator which does not affect functionality but it is used as marker
    which tells that this object is not interesting for users and it is only used internally 
    """
    return fn