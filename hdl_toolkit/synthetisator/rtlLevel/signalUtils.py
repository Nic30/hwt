from hdl_toolkit.synthetisator.interfaceLevel.interface import Interface
def connectSig(a, b):
    if isinstance(a, Interface):
        a = a._sig
    b._src = a
    return b._sig.assignFrom(a)