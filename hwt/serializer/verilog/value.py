from hwt.bitmask import mask
from hwt.hdlObjects.constants import DIRECTION
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import BOOL, BIT
from hwt.hdlObjects.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.value import GenericSerializer_Value
from hwt.serializer.serializerClases.indent import getIndent
from hwt.serializer.verilog.utils import SIGNAL_TYPE
from hwt.synthesizer.param import getParam
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class VerilogSerializer_Value(GenericSerializer_Value):

    @classmethod
    def BitLiteral(cls, v, vldMask):
        if vldMask:
            return "2'b%d" % int(bool(v))
        else:
            return "2'bx"

    @classmethod
    def BitString(cls, v, width, vldMask=None):
        if vldMask is None:
            vldMask = mask(width)
        # if can be in hex
        if width % 4 == 0 and vldMask == (1 << width) - 1:
            return ("%d'h%0" + str(width // 4) + 'x"') % (width, v)
        else:  # else in binary
            return cls.BitString_binary(v, width, vldMask)

    @staticmethod
    def BitString_binary(v, width, vldMask=None):
        buff = ["%d'b" % width]
        for i in range(width - 1, -1, -1):
            mask = (1 << i)
            b = v & mask

            if vldMask & mask:
                s = "1" if b else "0"
            else:
                s = "x"
            buff.append(s)
        return ''.join(buff)

    @classmethod
    def Bool_valAsHdl(cls, dtype, val, ctx):
        return str(int(val.val))

    @classmethod
    def DIRECTION(cls, d):
        if d is DIRECTION.IN:
            return "input"
        elif d is DIRECTION.OUT:
            return "output"
        elif d is DIRECTION.INOUT:
            return "inout"
        else:
            raise NotImplementedError(d)

    @classmethod
    def condAsHdl(cls, cond, forceBool, createTmpVarFn):
        if isinstance(cond, RtlSignalBase):
            cond = [cond]
        else:
            cond = list(cond)
        if len(cond) == 1:
            c = cond[0]
            if not forceBool or c._dtype == BOOL:
                return cls.asHdl(c, createTmpVarFn)
            elif c._dtype == BIT:
                return "(%s)==%s" % (cls.asHdl(c, createTmpVarFn), cls.BitLiteral(1, 1))
            elif isinstance(c._dtype, Bits):
                width = c._dtype.bit_length()
                return "(%s)!=%s" % (cls.asHdl(c, createTmpVarFn), cls.BitString(0, width))
            else:
                raise NotImplementedError()
        else:
            return " && ".join(map(lambda x: cls.condAsHdl(x, forceBool, createTmpVarFn), cond))


    @classmethod
    def SignalItem(cls, si, ctx, declaration=False):
        if declaration:
            ctx = ctx.forSignal(si)

            v = si.defaultVal
            prefix = ""
            if si.virtualOnly:
                pass
            elif si.drivers:
                pass
            elif si.endpoints or si.simSensProcs:
                if not v.vldMask:
                    raise SerializerException("Signal %s is constant and has undefined value" % si.name)
            else:
                raise SerializerException("Signal %s should be declared but it is not used" % si.name)

            s = "%s%s%s %s" % (getIndent(ctx.indent),
                               prefix,
                               cls.HdlType(si._dtype, ctx),
                               si.name)
            if isinstance(v, RtlSignalBase):
                return s + " = %s" % cls.asHdl(v, ctx)
            elif isinstance(v, Value):
                if si.defaultVal.vldMask:
                    return s + " = %s" % cls.Value(si.defaultVal, ctx)
                else:
                    return s
            else:
                raise NotImplementedError(v)

        else:
            if si.hidden and hasattr(si, "origin"):
                return cls.asHdl(si.origin, ctx)
            else:
                return si.name

    @classmethod
    def Slice_valAsHdl(cls, dtype, val, ctx):
        upper = val.val[0]
        if isinstance(upper, Value):
            upper = upper - 1
            _format = "%s:%s"
        else:
            _format = "%s-1:%s"

        return _format % (cls.Value(upper, ctx), cls.Value(val.val[1], ctx))

    @classmethod
    def sensitivityListItem(cls, item, createTmpVarFn, anyIsEventDependent):
        if isinstance(item, Operator):
            o = item.operator
            item = item.ops[0]
            if o is AllOps.RISING_EDGE:
                prefix = "posedge "
            elif o is AllOps.FALLIGN_EDGE:
                prefix = "negedge "
            else:
                raise NotImplementedError()
            return prefix + cls.asHdl(item, createTmpVarFn)
        elif anyIsEventDependent:
            if item.negated:
                prefix = "negedge "
            else:
                prefix = "posedge "

            return prefix + cls.asHdl(item, createTmpVarFn)

        return cls.asHdl(item, createTmpVarFn)

