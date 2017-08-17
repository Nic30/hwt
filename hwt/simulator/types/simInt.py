from hwt.hdlObjects.types.integer import Integer


class SimInteger(Integer):
    @classmethod
    def getConvertFn(cls):
        raise TypeError("There should not be any need to dynamically convert Integer in simulation")


SIM_INT = SimInteger()
# create hdl integer value (for example integer value in vhdl)


def simHInt(val):
    return SIM_INT.fromPy(val)
