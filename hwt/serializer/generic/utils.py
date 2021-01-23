from ipCorePackager.constants import DIRECTION
from hdlConvertorAst.hdlAst._expr import HdlDirection
from hwt.doc_markers import internal

HWT_TO_HDLCONVEROTR_DIRECTION = {
    DIRECTION.IN: HdlDirection.IN,
    DIRECTION.INOUT: HdlDirection.INOUT,
    DIRECTION.OUT: HdlDirection.OUT,
}


@internal
class TmpVarsSwap():
    """
    An object which is used as a context manager for tmpVars inside of :class:`~.ToHdlAst`
    """

    def __init__(self, ctx, tmpVars):
        self.ctx = ctx
        self.tmpVars = tmpVars

    def __enter__(self):
        self.orig = self.ctx.tmpVars
        self.ctx.tmpVars = self.tmpVars

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ctx.tmpVars = self.orig
