
class TypeConversionErr(TypeError):
    pass


class ConfErr(Exception):
    pass


class IntfLvlConfErr(ConfErr):
    """
    Interface level synthesizer user configuration error
    """
    pass


class SigLvlConfErr(ConfErr):
    """
    Signal level synthesizer user configuration error
    """
    pass
