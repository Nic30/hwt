from hdl_toolkit.intfLvl import UnitFromHdl

ws = "vhdl/fnImport/"

lib = [ws + "package0.vhd"]

class EntWithFnRequired(UnitFromHdl):
    _hdlSources = [ws + "ent.vhd"] + lib

 
if __name__ == "__main__":
    from hdl_toolkit.synthetisator.shortcuts import toRtl
    u = EntWithFnRequired()
    u._loadDeclarations()
    print(u)
    print(u.sig._dtype.getBitCnt())
    # print(synthetizeCls(EntWithFnRequired))
