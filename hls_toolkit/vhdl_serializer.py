from vhdl_toolkit.entity import Entity, PortItem, VHDLType, VHDLExtraType
from vhdl_toolkit.architecture import Architecture

def serializeComponent(comp):
    ent = Entity()
    ent.name = comp.name
    ent.port.extend(comp.port)
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
    clk = PortItem("clk", PortItem.typeIn, t)
    e = Entity()
    e.port.append(clk)
    e.name = "enr1"
    extraTypes = [enum]
    a = Architecture(e.name , extraTypes, [], [], [])
    print(str(e))
    print(str(a))
