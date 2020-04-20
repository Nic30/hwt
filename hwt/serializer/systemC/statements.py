from hdlConvertor.to.verilog.constants import SIGNAL_TYPE
from hwt.doc_markers import internal
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL
from hwt.hdl.variables import SignalItem
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.systemC.utils import systemCTypeOfSig


class ToHdlAstSystemC_statements():

    @internal
    def _as_hdl_Assignment(self, dst, typeOfDst, src):

        dstStr = self.as_hdl(dst.forTarget())
        if typeOfDst == SIGNAL_TYPE.REG:
            fmt = "%s%s = %s;"
        else:
            fmt = "%s%s.write(%s);"

        return fmt % (dstStr, self.Value(src))

    def as_hdl_Assignment(self, a):
        dst = a.dst
        assert isinstance(dst, SignalItem)
        assert not dst.virtual_only, "should not be required"

        typeOfDst = systemCTypeOfSig(dst)
        if a.indexes is not None:
            for i in reversed(a.indexes):
                dst = dst[i]

        if dst._dtype == a.src._dtype or (
                isinstance(dst._dtype, Bits) and a.src._dtype == BOOL):
            return self._as_hdl_Assignment(dst, typeOfDst, a.src)
        else:
            raise SerializerException("%r <= %r  is not valid assignment\n"
                                      " because types are different (%r; %r) "
                                      % (dst, a.src, dst._dtype, a.src._dtype))
