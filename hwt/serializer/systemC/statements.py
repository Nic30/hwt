from hwt.serializer.serializerClases.indent import getIndent
from hwt.hdlObjects.variables import SignalItem
from hwt.hdlObjects.types.bits import Bits
from hwt.serializer.exceptions import SerializerException


class SystemCSerializer_statements():

    @classmethod
    def _Assignment(cls, dst, src, ctx):
        indent_str = getIndent(ctx.indent)
        def valAsHdl(v):
            return cls.Value(v, ctx)
        
        dstStr = cls.asHdl(dst, ctx.forTarget())
        return "%s%s.write(%s);" % (indent_str, dstStr, valAsHdl(src))

    @classmethod
    def Assignment(cls, a, ctx):
        dst = a.dst
        assert isinstance(dst, SignalItem)
        assert not dst.virtualOnly, "should not be required"

        if a.indexes is not None:
            for i in a.indexes:
                dst = dst[i]

        if dst._dtype == a.src._dtype:
            return cls._Assignment(dst, a.src, ctx)
        else:
            srcT = a.src._dtype
            dstT = dst._dtype
            if isinstance(srcT, Bits) and isinstance(dstT, Bits):
                sLen = srcT.bit_length()
                dLen = dstT.bit_length()
                if sLen == dLen:
                    if sLen == 1 and srcT.forceVector != dstT.forceVector:
                        if srcT.forceVector:
                            return cls._Assignment(dst, a.src[0], ctx)
                        else:
                            return cls._Assignment(dst[0], a.src, ctx)
                    elif srcT.signed is not dstT.signed:
                        return cls._Assignment(dst, a.src._convSign(dstT.signed), ctx)
                
            raise SerializerException("%r <= %r  is not valid assignment\n because types are different (%r; %r) " % 
                                      (dst, a.src, dst._dtype, a.src._dtype))

    
    @classmethod
    def HWProcess(cls, proc, ctx):
        """
        Serialize HWProcess instance

        :param scope: name scope to prevent name collisions
        """
        body = proc.statements
        childCtx = ctx.withIndent()
        statemets = [cls.asHdl(s, childCtx) for s in body]
        proc.name = ctx.scope.checkedName(proc.name, proc)

        return cls.methodTmpl.render(
            indent=getIndent(ctx.indent),
            name=proc.name,
            statements=statemets
            )
