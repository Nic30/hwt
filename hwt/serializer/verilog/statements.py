from hwt.hdl.assignment import Assignment
from hwt.hdl.operator import Operator
from hwt.hdl.process import HWProcess
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.variables import SignalItem
from hwt.pyUtils.arrayQuery import arr_any
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.constants import SIGNAL_TYPE
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.verilog.utils import verilogTypeOfSig
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class VerilogSerializer_statements():
    @classmethod
    def Assignment(cls, a: Assignment, ctx):
        dst = a.dst
        assert isinstance(dst, SignalItem)

        def valAsHdl(v):
            return cls.Value(v, ctx)

        # dstSignalType = verilogTypeOfSig(dst)
        indent_str = getIndent(ctx.indent)
        _dst = dst
        if a.indexes is not None:
            for i in a.indexes:
                if isinstance(i, SliceVal):
                    i = i.__copy__()
                    i.val = (i.val[0], i.val[1])
                dst = dst[i]
        dstStr = cls.asHdl(dst, ctx)
        srcStr = valAsHdl(a.src)

        ver_sig_t = verilogTypeOfSig(_dst)
        if ver_sig_t == SIGNAL_TYPE.REG:
            evDep = False
            for driver in _dst.drivers:
                if driver._now_is_event_dependent:
                    evDep = True
                    break

            if not evDep or _dst.virtualOnly:
                prefix = ""
                symbol = "="
            else:
                prefix = ""
                symbol = "<="
        elif ver_sig_t == SIGNAL_TYPE.WIRE:
            if a.parentStm is None:
                prefix = "assign "
            else:
                prefix = ""
            symbol = "="
        else:
            ValueError(ver_sig_t)

        firstPartOfStr = "%s%s%s" % (indent_str, prefix, dstStr)
        src_t = a.src._dtype
        dst_t = dst._dtype

        if dst_t == src_t \
            or (isinstance(src_t, Bits)
                and isinstance(dst_t, Bits)
                and src_t.bit_length() == dst_t.bit_length() == 1):
            return "%s %s %s;" % (firstPartOfStr, symbol, srcStr)
        else:
            raise SerializerException("%s %s %s is not valid assignment\n"
                                      " because types are different (%r; %r) "
                                      % (dstStr, symbol, srcStr,
                                         dst._dtype, a.src._dtype))

    @classmethod
    def HWProcess(cls, proc: HWProcess, ctx):
        """
        Serialize HWProcess objects
        """
        body = proc.statements
        extraVars = []
        extraVarsSerialized = []

        anyIsEventDependnt = arr_any(
            proc.sensitivityList, lambda s: isinstance(s, Operator))
        sensitivityList = sorted(
            map(lambda s: cls.sensitivityListItem(s, ctx,
                                                  anyIsEventDependnt),
                proc.sensitivityList))

        hasToBeProcess = arr_any(
            proc.outputs,
            lambda x: verilogTypeOfSig(x) == SIGNAL_TYPE.REG
        )

        if hasToBeProcess:
            childCtx = ctx.withIndent()
        else:
            childCtx = ctx

        def createTmpVarFn(suggestedName, dtype):
            s = RtlSignal(None, None, dtype, virtualOnly=True)
            s.name = childCtx.scope.checkedName(suggestedName, s)
            s.hidden = False
            serializedS = cls.SignalItem(s, childCtx, declaration=True)
            extraVars.append(s)
            extraVarsSerialized.append(serializedS)
            return s

        childCtx.createTmpVarFn = createTmpVarFn
        statemets = [cls.asHdl(s, childCtx) for s in body]

        if hasToBeProcess:
            proc.name = ctx.scope.checkedName(proc.name, proc)

        extraVarsInit = []
        for s in extraVars:
            a = Assignment(s.defVal, s, virtualOnly=True)
            extraVarsInit.append(cls.Assignment(a, childCtx))

        return cls.processTmpl.render(
            indent=getIndent(ctx.indent),
            name=proc.name,
            hasToBeProcess=hasToBeProcess,
            extraVars=extraVarsSerialized,
            sensitivityList=" or ".join(sensitivityList),
            statements=extraVarsInit + statemets
        )
