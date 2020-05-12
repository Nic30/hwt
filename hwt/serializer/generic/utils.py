from ipCorePackager.constants import DIRECTION
from hdlConvertorAst.hdlAst._expr import HdlDirection
from hwt.doc_markers import internal


HWT_TO_HDLCONVEROTR_DIRECTION = {
    DIRECTION.IN: HdlDirection.IN,
    DIRECTION.INOUT: HdlDirection.INOUT,
    DIRECTION.OUT: HdlDirection.OUT,
}


@internal
class CreateTmpVarFnSwap():
    """
    An object which is used as a context manager for createTmpVarFn inside of :class:`~.ToHdlAst`
    """

    def __init__(self, ctx, createTmpVarFn):
        self.ctx = ctx
        self.createTmpVarFn = createTmpVarFn

    def __enter__(self):
        self.orig = self.ctx.createTmpVarFn
        self.ctx.createTmpVarFn = self.createTmpVarFn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ctx.createTmpVarFn = self.orig
