from vhdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls

ws = "vhdl/fnImport/"

class EntWithFnRequired(UnitFromHdl):
    _hdlSources = [ws + "ent.vhd", ws + "package0.vhd"]

 
if __name__ == "__main__":
    u = EntWithFnRequired()
    print(u)
    print(u.sig._dtype.getBitCnt())
    # print(synthetizeCls(EntWithFnRequired))
