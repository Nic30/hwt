from hwt.hdlObjects.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.value import GenericSerializer_Value
from hwt.serializer.serializerClases.indent import getIndent
from hwt.serializer.verilog.utils import verilogTypeOfSig, SIGNAL_TYPE
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.bitmask import mask
from hwt.hdlObjects.constants import DIRECTION
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.types.defs import BOOL, BIT
from hwt.hdlObjects.types.bits import Bits


class VerilogSerializer_Value(GenericSerializer_Value):

    @classmethod
    def SignalItem(cls, si, createTmpVarFn, declaration=False, indent=0):
        if declaration:
            st = verilogTypeOfSig(si)

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

            s = "%s%s%s %s" % (getIndent(indent),
                               prefix,
                               cls.HdlType(si._dtype, createTmpVarFn, st),
                               si.name)
            if isinstance(v, RtlSignalBase):
                return s + " = %s" % cls.asHdl(v, createTmpVarFn)
            elif isinstance(v, Value):
                if si.defaultVal.vldMask:
                    return s + " = %s" % cls.Value(si.defaultVal, createTmpVarFn)
                else:
                    return s
            else:
                raise NotImplementedError(v)

        else:
            assert indent == 0
            if si.hidden and hasattr(si, "origin"):
                return cls.asHdl(si.origin, createTmpVarFn)
            else:
                return si.name

    @classmethod
    def Slice_valAsHdl(cls, dtype, val, createTmpVarFn):
        return "%s:%s" % (cls.Value(val.val[0], createTmpVarFn), cls.Value(val.val[1], createTmpVarFn))

    @classmethod
    def BitString(cls, v, width, vldMask=None):
        if vldMask is None:
            vldMask = mask(width)
        # if can be in hex
        if width % 4 == 0 and vldMask == (1 << width) - 1:
            return ("16'b%0" + str(width // 4) + 'x"') % (v)
        else:  # else in binary
            return cls.BitString_binary(v, width, vldMask)

    @classmethod
    def BitLiteral(cls, v, vldMask):
        if vldMask:
            return "2'b%d" % int(bool(v))
        else:
            return "2'bx"

    @staticmethod
    def BitString_binary(v, width, vldMask=None):
        buff = []
        for i in range(width - 1, -1, -1):
            mask = (1 << i)
            b = v & mask

            if vldMask & mask:
                s = "1" if b else "0"
            else:
                s = "x"
            buff.append(s)
        return "2'b%s" % (''.join(buff))

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

    @classmethod
    def PortItem(cls, pi, createTmpVarFn):
        return "%s %s %s" % (cls.DIRECTION(pi.direction),
                             cls.HdlType(pi._dtype, createTmpVarFn, SIGNAL_TYPE.PORT),
                             pi.name)

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
