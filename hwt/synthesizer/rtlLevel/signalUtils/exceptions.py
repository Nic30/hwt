

class MultipleDriversErr(Exception):
    """
    Signal has multiple combinational drivers, this is not possible in real word
    """
    pass


class NoDriverErr(Exception):
    """
    Signal has no driver specified and it drives something which has effect on output
    """
    pass
