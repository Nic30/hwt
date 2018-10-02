from hwt.hdl.types.integer import Integer
from hwt.doc_markers import internal


@internal
class SimInteger(Integer):
    @classmethod
    def getConvertFn(cls):
        raise TypeError("There should not be any need to dynamically convert"
                        "Integer in simulation")


SIM_INT = SimInteger()
# create hdl integer value (for example integer value in vhdl)


@internal
def simHInt(val):
    return SIM_INT.fromPy(val)
