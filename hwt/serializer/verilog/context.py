from copy import copy

from hwt.serializer.serializerClases.context import SerializerCtx
from hwt.serializer.verilog.utils import verilogTypeOfSig, SIGNAL_TYPE


class VerilogSerializerCtx(SerializerCtx):
    """
    :ivar signalType: member of SIGNAL_TYPE
    """

    def forPort(self):
        ctx = copy(self)
        ctx.signalType = SIGNAL_TYPE.PORT
        return ctx

    def forSignal(self, signalItem):
        ctx = copy(self)
        ctx.signalType = verilogTypeOfSig(signalItem)
        return ctx
