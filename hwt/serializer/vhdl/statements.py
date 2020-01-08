from copy import copy

from hwt.doc_markers import internal
from hwt.hdl.assignment import Assignment
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.value import Value
from hwt.hdl.variables import SignalItem
from hwt.hdl.waitStm import WaitStm
from hwt.hdl.whileContainer import WhileContainer
from hwt.pyUtils.arrayQuery import arr_any
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.vhdl.utils import VhdlVersion
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversErr, \
    NoDriverErr


@internal
class DoesNotContainsTernary(Exception):
    pass


@internal
def ternaryOpsToIf(statements):
    """Convert all ternary operators to IfContainers"""
    stms = []

    for st in statements:
        if isinstance(st, Assignment):
            try:
                if not isinstance(st.src, RtlSignalBase):
                    raise DoesNotContainsTernary()
                d = st.src.singleDriver()
                if not isinstance(d, Operator) or d.operator != AllOps.TERNARY:
                    raise DoesNotContainsTernary()
                else:
                    ops = d.operands
                    ifc = IfContainer(ops[0],
                                      [Assignment(ops[1], st.dst)],
                                      [Assignment(ops[2], st.dst)]
                                      )
                    stms.append(ifc)
                    continue

            except (MultipleDriversErr, DoesNotContainsTernary):
                pass
            except NoDriverErr:
                assert (hasattr(st.src, "_interface")
                        and st.src._interface is not None)\
                    or st.src.def_val.vld_mask, st.src

        stms.append(st)
    return stms


class VhdlSerializer_statements():

    @classmethod
    def Assignment(cls, a, ctx):
        dst = a.dst
        assert isinstance(dst, SignalItem)

        def valAsHdl(v):
            return cls.Value(v, ctx)

        if dst.virtual_only:
            symbol = ":="
        else:
            symbol = "<="

        if a.indexes is not None:
            for i in reversed(a.indexes):
                if isinstance(i, SliceVal):
                    i = i.__copy__()
                dst = dst[i]

        indent_str = getIndent(ctx.indent)
        dstStr = cls.asHdl(dst, ctx)
        src_t = a.src._dtype
        dst_t = dst._dtype

        if dst_t == src_t:
            return "%s%s %s %s" % (indent_str, dstStr, symbol, valAsHdl(a.src))
        else:
            correct = False
            src = a.src
            if (isinstance(dst_t, Bits)
                    and isinstance(src_t, Bits)):
                if dst_t.bit_length() == src_t.bit_length() == 1:
                    if dst_t.force_vector and not src_t.force_vector:
                        dstStr = "%s(0)" % (dstStr)
                        srcStr = valAsHdl(a.src)
                        correct = True
                    elif not dst_t.force_vector and src_t.force_vector:
                        srcStr = "%s(0)" % valAsHdl(src)
                        correct = True
                    elif src_t == BOOL:
                        srcStr = "'1' WHEN %s ELSE '0'" % valAsHdl(src)
                        correct = True
                elif not src_t.strict_width:
                    if isinstance(src, Value):
                        _src = copy(src)
                        if a.indexes:
                            raise NotImplementedError()

                        _src._dtype = dst_t
                        srcStr = cls.Value(_src, ctx)
                        correct = True
                    else:
                        raise NotImplementedError()
                        pass

            if correct:
                return "%s%s %s %s" % (indent_str, dstStr, symbol, srcStr)

            raise SerializerException(
                "%s%s %s %s  is not valid assignment\n"
                " because types are different (%r; %r) " % 
                (indent_str, dstStr, symbol, valAsHdl(a.src),
                 dst._dtype, a.src._dtype))

    @classmethod
    def HWProcess(cls, proc, ctx):
        """
        Serialize HWProcess objects as VHDL

        :param scope: name scope to prevent name collisions
        """
        body = proc.statements
        extraVars = []
        extraVarsSerialized = []

        hasToBeVhdlProcess = arr_any(body,
                                     lambda x: isinstance(x,
                                                          (IfContainer,
                                                           SwitchContainer,
                                                           WhileContainer,
                                                           WaitStm)))

        sensitivityList = sorted(
            map(lambda s: cls.sensitivityListItem(s, ctx),
                proc.sensitivityList))

        if hasToBeVhdlProcess:
            childCtx = ctx.withIndent()
        else:
            childCtx = copy(ctx)

        def createTmpVarFn(suggestedName, dtype):
            s = RtlSignal(None, None, dtype, virtual_only=True)
            s.name = ctx.scope.checkedName(suggestedName, s)
            s.hidden = False
            serializedS = cls.SignalItem(s, childCtx, declaration=True)
            extraVars.append(s)
            extraVarsSerialized.append(serializedS)
            return s

        childCtx.createTmpVarFn = createTmpVarFn

        statemets = [cls.asHdl(s, childCtx) for s in body]
        proc.name = ctx.scope.checkedName(proc.name, proc)

        extraVarsInit = []
        for s in extraVars:
            if isinstance(s.def_val, RtlSignalBase) or s.def_val.vld_mask:
                a = Assignment(s.def_val, s, virtual_only=True)
                extraVarsInit.append(cls.Assignment(a, childCtx))
            else:
                assert s.drivers, s
            for d in s.drivers:
                extraVarsInit.append(cls.asHdl(d, childCtx))

        _hasToBeVhdlProcess = hasToBeVhdlProcess
        hasToBeVhdlProcess = extraVars or hasToBeVhdlProcess

        if hasToBeVhdlProcess and not _hasToBeVhdlProcess:
            # add indent because we did not added it before because we did not
            # know t
            oneIndent = getIndent(1)
            statemets = [oneIndent + x for x in statemets]

        return cls.processTmpl.render(
            indent=getIndent(ctx.indent),
            name=proc.name,
            hasToBeVhdlProcess=hasToBeVhdlProcess,
            extraVars=extraVarsSerialized,
            sensitivityList=", ".join(sensitivityList),
            statements=extraVarsInit + statemets
        )

    @classmethod
    def IfContainer(cls, ifc: IfContainer, ctx):
        childCtx = ctx.withIndent()

        def asHdl(statements):
            return [cls.asHdl(s, childCtx) for s in statements]

        cond = cls.condAsHdl(ifc.cond, True, childCtx)
        elIfs = []
        if ifc.ifFalse is not None:
            ifFalse = ifc.ifFalse
        else:
            ifFalse = []
        ifTrue = ifc.ifTrue

        if cls.VHDL_VER < VhdlVersion.v2008:
            ifTrue = ternaryOpsToIf(ifTrue)
            ifFalse = ternaryOpsToIf(ifFalse)

        for c, statements in ifc.elIfs:
            if cls.VHDL_VER < VhdlVersion.v2008:
                statements = ternaryOpsToIf(statements)

            elIfs.append((cls.condAsHdl(c, True, childCtx), asHdl(statements)))

        return cls.ifTmpl.render(
            indent=getIndent(ctx.indent),
            cond=cond,
            ifTrue=asHdl(ifTrue),
            elIfs=elIfs,
            ifFalse=asHdl(ifFalse))

    @classmethod
    def SwitchContainer(cls, sw, ctx):
        childCtx = ctx.withIndent()

        def asHdl(statements):
            return [cls.asHdl(s, childCtx) for s in statements]

        switchOn = cls.condAsHdl(sw.switchOn, False, ctx)

        cases = []
        for key, statements in sw.cases:
            key = cls.asHdl(key, ctx)

            if cls.VHDL_VER < VhdlVersion.v2008:
                statements = ternaryOpsToIf(statements)

            cases.append((key, asHdl(statements)))

        if sw.default:
            cases.append((None, asHdl(sw.default)))

        return cls.switchTmpl.render(
            indent=getIndent(ctx.indent),
            switchOn=switchOn,
            cases=cases)

    @classmethod
    def WaitStm(cls, w, ctx):
        indent_str = getIndent(ctx.indent)

        if w.isTimeWait:
            return "%swait for %d ns" % (indent_str, w.waitForWhat)
        elif w.waitForWhat is None:
            return "%swait" % indent_str
        else:
            raise NotImplementedError()
