
class NOT_SPECIFIED():
    """
    Constant which means that the thing is not specified

    Used for optional argumens as a value whchi marks that the value of this
    argument was not specified on the place where we can not just use None
    """
    def __init__(self):
        raise AssertionError("Use only a class a constant")