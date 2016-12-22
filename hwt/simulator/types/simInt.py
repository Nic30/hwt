from hwt.hdlObjects.types.integer import Integer


class SimInteger(Integer):
    @classmethod
    def getConvertor(cls):
        from hwt.simulator.types.simIntConversions import convertSimInteger__val
        return convertSimInteger__val        


SIM_INT = SimInteger()
# create hdl integer value (for example integer value in vhdl)
simHInt = lambda val: SIM_INT.fromPy(val)