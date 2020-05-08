from hdlConvertorAst.to.verilog.constants import SIGNAL_TYPE


class SignalTypeSwap():
    """
    An object which is used as a context manager for signalType
    inside of :class:`hwt.serializer.verilog.serializer.ToHdlAstVerilog`
    """

    def __init__(self, ctx, signalType: SIGNAL_TYPE):
        self.ctx = ctx
        self.signalType = signalType

    def __enter__(self):
        self.orig = self.ctx.createTmpVarFn
        self.ctx.signalType = self.signalType

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ctx.signalType = self.orig
