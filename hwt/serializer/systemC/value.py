from hwt.hdlObjects.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.value import GenericSerializer_Value
from hwt.serializer.serializerClases.indent import getIndent
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class SystemCSerializer_value(GenericSerializer_Value):
    
    @classmethod
    def SignalItem(cls, si, createTmpVarFn, scope, declaration=False, indent=0):
        if declaration:
            v = si.defaultVal
            if si.virtualOnly:
                prefix = "VARIABLE"
            elif si.drivers:
                prefix = "SIGNAL"
            elif si.endpoints or si.simSensProcs:
                prefix = "CONSTANT"
                if not v.vldMask:
                    raise SerializerException("Signal %s is constant and has undefined value" % si.name)
            else:
                raise SerializerException("Signal %s should be declared but it is not used" % si.name)

            s = "%s%s %s : %s" % (getIndent(indent), prefix, si.name, cls.HdlType(si._dtype, createTmpVarFn))
            if isinstance(v, RtlSignalBase):
                return s + " := %s" % cls.asHdl(v, createTmpVarFn)
            elif isinstance(v, Value):
                if si.defaultVal.vldMask:
                    return s + " := %s" % cls.Value(si.defaultVal, createTmpVarFn)
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