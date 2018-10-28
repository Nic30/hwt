from hwt.hdl.assignment import Assignment
from hwt.hdl.operator import Operator
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.variables import SignalItem
from hwt.pyUtils.arrayQuery import arr_any
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.indent import getIndent
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.whileContainer import WhileContainer
from hwt.hdl.waitStm import WaitStm


class VerilogSerializer_statements():
    @classmethod
    def Assignment(cls, a: Assignment, ctx):
        dst = a.dst
        assert isinstance(dst, SignalItem)

        def valAsHdl(v):
            return cls.Value(v, ctx)

        # dstSignalType = verilogTypeOfSig(dst)

        assert not dst.virtualOnly
        if a._is_completly_event_dependent:
            prefix = ""
            symbol = "<="
        else:
            if a.parentStm is None:
                prefix = "assign "
            else:
                prefix = ""
            symbol = "="

        if a.indexes is not None:
            for i in a.indexes:
                if isinstance(i, SliceVal):
                    i = i.clone()
                    i.val = (i.val[0], i.val[1])
                dst = dst[i]

        indent_str = getIndent(ctx.indent)
        dstStr = cls.asHdl(dst, ctx)
        firstPartOfStr = "%s%s%s" % (indent_str, prefix, dstStr)
        src_t = a.src._dtype
        dst_t = dst._dtype

        if dst_t == src_t \
            or (isinstance(src_t, Bits)
                and isinstance(dst_t, Bits)
                and src_t.bit_length() == dst_t.bit_length() == 1):
            return "%s %s %s;" % (firstPartOfStr, symbol, valAsHdl(a.src))
        else:
            raise SerializerException("%s %s %s is not valid assignment\n"
                                      " because types are different (%r; %r) "
                                      % (dstStr, symbol, valAsHdl(a.src),
                                         dst._dtype, a.src._dtype))

    @classmethod
    def HWProcess(cls, proc, ctx):
        """
        Serialize HWProcess objects
        """
        body = proc.statements
        extraVars = []
        extraVarsSerialized = []

        hasToBeVhdlProcess = extraVars or\
            arr_any(body,
                    lambda x: isinstance(x,
                                         (IfContainer,
                                          SwitchContainer,
                                          WhileContainer,
                                          WaitStm)) or
                    (isinstance(x, Assignment) and
                     x.indexes))

        anyIsEventDependnt = arr_any(
            proc.sensitivityList, lambda s: isinstance(s, Operator))
        sensitivityList = sorted(
            map(lambda s: cls.sensitivityListItem(s, ctx,
                                                  anyIsEventDependnt),
                proc.sensitivityList))

        if hasToBeVhdlProcess:
            childCtx = ctx.withIndent()
        else:
            childCtx = ctx

        def createTmpVarFn(suggestedName, dtype):
            # [TODO] it is better to use RtlSignal
            s = SignalItem(None, dtype, virtualOnly=True)
            s.name = childCtx.scope.checkedName(suggestedName, s)
            s.hidden = False
            serializedS = cls.SignalItem(s, childCtx, declaration=True)
            extraVars.append(s)
            extraVarsSerialized.append(serializedS)
            return s

        childCtx.createTmpVarFn = createTmpVarFn

        statemets = [cls.asHdl(s, childCtx) for s in body]

        if hasToBeVhdlProcess:
            proc.name = ctx.scope.checkedName(proc.name, proc)

        extraVarsInit = []
        for s in extraVars:
            a = Assignment(s.defVal, s, virtualOnly=True)
            extraVarsInit.append(cls.Assignment(a, childCtx))

        return cls.processTmpl.render(
            indent=getIndent(ctx.indent),
            name=proc.name,
            hasToBeVhdlProcess=hasToBeVhdlProcess,
            extraVars=extraVarsSerialized,
            sensitivityList=" or ".join(sensitivityList),
            statements=extraVarsInit + statemets
        )
