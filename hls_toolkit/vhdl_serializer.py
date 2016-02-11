"""
@attention:  Not used yet
"""

from hls_toolkit.syntetizator_config import HLSSyntetizatorConfig as config
from vhdl_toolkit.hdlObjects.architecture import Architecture
from vhdl_toolkit.hdlObjects.entity import Entity
from vhdl_toolkit.hdlObjects.variables import PortItem
from vhdl_toolkit.types import VHDLType, VHDLExtraType, DIRECTION


def portFromVariables(variables):
    port = []
    for v in variables:
        v.typ.name = v.name
        v.typ.direction = DIRECTION.IN
        port.extend(v.typ.asPortItems())
    return port

def serializeComponent(comp):
    ent = Entity()
    ent.name = comp.name
    ent.port.extend(portFromVariables(comp.port))
    variables = []
    eTypes = []
    processes = []
    components = []
    arch = Architecture(ent.name, variables, eTypes , processes, components)
    return "\n".join([str(ent), str(arch)])

if __name__ == "__main__":
    t = VHDLType()
    enum = VHDLExtraType.createEnum("enum0", ["val0", "val1", "val3"])
    t.str = "std_logic_vector(0 downto 15)"
    clk = PortItem("clk", DIRECTION.IN, t)
    e = Entity()
    e.port.append(clk)
    e.name = "enr1"
    extraTypes = [enum]
    a = Architecture(e.name , extraTypes, [], [], [])
    print(str(e))
    print(str(a))
