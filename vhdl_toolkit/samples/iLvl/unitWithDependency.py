from vhdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls

ws = "vhdl/fnImport/"

lib = [ws + "package0.vhd"]

class EntWithFnRequired(UnitFromHdl):
    _hdlSources = [ws + "ent.vhd"] + lib

 
if __name__ == "__main__":
    u = EntWithFnRequired()
    u._loadDeclarations()
    print(u)
    print(u.sig._dtype.getBitCnt())
    # print(synthetizeCls(EntWithFnRequired))
