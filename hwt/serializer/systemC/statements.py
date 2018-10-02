from hwt.hdl.variables import SignalItem
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.constants import SIGNAL_TYPE
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.systemC.utils import systemCTypeOfSig
from hwt.doc_markers import internal


class SystemCSerializer_statements():

    @internal
    @classmethod
    def _Assignment(cls, dst, typeOfDst, src, ctx):
        indent_str = getIndent(ctx.indent)

        dstStr = cls.asHdl(dst, ctx.forTarget())
        if typeOfDst == SIGNAL_TYPE.REG:
            fmt = "%s%s = %s;"
        else:
            fmt = "%s%s.write(%s);"

        return fmt % (indent_str, dstStr, cls.Value(src, ctx))

    @classmethod
    def Assignment(cls, a, ctx):
        dst = a.dst
        assert isinstance(dst, SignalItem)
        assert not dst.virtualOnly, "should not be required"

        typeOfDst = systemCTypeOfSig(dst)
        if a.indexes is not None:
            for i in a.indexes:
                dst = dst[i]

        if dst._dtype == a.src._dtype:
            return cls._Assignment(dst, typeOfDst, a.src, ctx)
        else:
            raise SerializerException("%r <= %r  is not valid assignment\n"
                                      " because types are different (%r; %r) "
                                      % (dst, a.src, dst._dtype, a.src._dtype))

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
