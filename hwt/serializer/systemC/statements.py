from hwt.hdlObjects.variables import SignalItem
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.serializerClases.indent import getIndent


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
            raise SerializerException("%r <= %r  is not valid assignment\n"
                                      " because types are different (%r; %r) " % 
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
