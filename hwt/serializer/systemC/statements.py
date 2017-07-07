from hwt.serializer.serializerClases.indent import getIndent
from hwt.hdlObjects.variables import SignalItem
from hwt.hdlObjects.types.sliceVal import SliceVal
from hwt.hdlObjects.types.bits import Bits
from hwt.serializer.exceptions import SerializerException


class SystemCSerializer_statements():

    @classmethod
    def Assignment(cls, a, ctx):
        dst = a.dst
        assert isinstance(dst, SignalItem)

        def valAsHdl(v):
            return cls.Value(v, ctx)

        assert not dst.virtualOnly, "should not be required"

        if a.indexes is not None:
            for i in a.indexes:
                raise NotImplementedError()
                # if isinstance(i, SliceVal):
                #    i = i.clone()
                #    i.val = (i.val[0], i.val[1])
                # dst = dst[i]

        indent_str = getIndent(ctx.indent)
        dstStr = dst.name
        if dst._dtype == a.src._dtype:
            return "%s%s.write(%s);" % (indent_str, dstStr, valAsHdl(a.src))
        else:
            # srcT = a.src._dtype
            # dstT = dst._dtype
            # if isinstance(srcT, Bits) and isinstance(dstT, Bits):
            #    sLen = srcT.bit_length()
            #    dLen = dstT.bit_length()
            #    if sLen == dLen:
            #        if sLen == 1 and srcT.forceVector != dstT.forceVector:
            #            if srcT.forceVector:
            #                return "%s%s %s %s(0)" % (indent_str, dstStr, symbol, valAsHdl(a.src))
            #            else:
            #                return "%s%s(0) %s %s" % (indent_str, dstStr, symbol, valAsHdl(a.src))
            #        elif srcT.signed is not dstT.signed:
            #            return "%s, %s %s %s" % (indent_str, dstStr, symbol, valAsHdl(a.src._convSign(dstT.signed)))
            #
            raise SerializerException("%s%s <= %s  is not valid assignment\n because types are different (%s; %s) " % 
                                      (indent_str, dstStr, valAsHdl(a.src), repr(dst._dtype), repr(a.src._dtype)))

    
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
