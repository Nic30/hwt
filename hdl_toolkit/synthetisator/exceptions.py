
class TypeConversionErr(Exception):
    pass

class ConfErr(Exception):
    pass

class IntfLvlConfErr(ConfErr):
    """
    Interface level synthetisator user configuration error
    """
    pass

class SigLvlConfErr(ConfErr):
    """
    Signal level synthetisator user configuration error
    """
    pass