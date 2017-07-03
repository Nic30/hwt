from copy import copy

from hwt.hdlObjects.assignment import Assignment
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.statements import IfContainer, SwitchContainer, \
    WhileContainer, WaitStm
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import BOOL, BIT
from hwt.hdlObjects.types.sliceVal import SliceVal
from hwt.hdlObjects.variables import SignalItem
from hwt.pyUtils.arrayQuery import arr_any
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.serializerClases.indent import getIndent
from hwt.serializer.vhdl.utils import VhdlVersion
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc


class DoesNotContainsTernary(Exception):
    pass


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
                    ifc = IfContainer(d.ops[0],
                                      [Assignment(d.ops[1], st.dst)],
                                      [Assignment(d.ops[2], st.dst)]
                                      )
                    stms.append(ifc)

            except (MultipleDriversExc, DoesNotContainsTernary):
                stms.append(st)
        else:
            stms.append(st)
    return stms


class VhdlSerializer_statements():

    @classmethod
    def condAsHdl(cls, cond, forceBool, ctx):
        if isinstance(cond, RtlSignalBase):
            cond = [cond]
        else:
            cond = list(cond)
        if len(cond) == 1:
            c = cond[0]
            if not forceBool or c._dtype == BOOL:
                return cls.asHdl(c, ctx)
            elif c._dtype == BIT:
                return "(" + cls.asHdl(c, ctx) + ")=" + cls.BitLiteral(1, 1)
            elif isinstance(c._dtype, Bits):
                width = c._dtype.bit_length()
                return "(" + cls.asHdl(c, ctx) + ")/=" + cls.BitString(0, width)
            else:
                raise NotImplementedError()
        else:
            return " AND ".join(map(lambda x: cls.condAsHdl(x, forceBool, ctx), cond))

    @classmethod
    def WaitStm(cls, w, ctx):
        indent_str = getIndent(ctx.indent)

        if w.isTimeWait:
            return "%swait for %d ns" % (indent_str, w.waitForWhat)
        elif w.waitForWhat is None:
            return "%swait" % indent_str
        else:
            raise NotImplementedError()

    @classmethod
    def Assignment(cls, a, ctx):
        dst = a.dst
        assert isinstance(dst, SignalItem)

        def valAsHdl(v):
            return cls.Value(v, ctx)

        if dst.virtualOnly:
            symbol = ":="
        else:
            symbol = "<="

        if a.indexes is not None:
            for i in a.indexes:
                if isinstance(i, SliceVal):
                    i = i.clone()
                    i.val = (i.val[0], i.val[1])
                dst = dst[i]

        indent_str = getIndent(ctx.indent)
        dstStr = cls.asHdl(dst, ctx)
        if dst._dtype == a.src._dtype:
            return "%s%s %s %s" % (indent_str, dstStr, symbol, valAsHdl(a.src))
        else:
            srcT = a.src._dtype
            dstT = dst._dtype
            if isinstance(srcT, Bits) and isinstance(dstT, Bits):
                sLen = srcT.bit_length()
                dLen = dstT.bit_length()
                if sLen == dLen:
                    if sLen == 1 and srcT.forceVector != dstT.forceVector:
                        if srcT.forceVector:
                            return "%s%s %s %s(0)" % (indent_str, dstStr, symbol, valAsHdl(a.src))
                        else:
                            return "%s%s(0) %s %s" % (indent_str, dstStr, symbol, valAsHdl(a.src))
                    elif srcT.signed is not dstT.signed:
                        return "%s, %s %s %s" % (indent_str, dstStr, symbol, valAsHdl(a.src._convSign(dstT.signed)))

            raise SerializerException("%s%s %s %s  is not valid assignment\n because types are different (%s; %s) " %
                                      (indent_str, dstStr, symbol, valAsHdl(a.src), repr(dst._dtype), repr(a.src._dtype)))

    @classmethod
    def IfContainer(cls, ifc, ctx):
        childCtx = ctx.withIndent()

        def asHdl(statements):
            return [cls.asHdl(s, childCtx) for s in statements]

        cond = cls.condAsHdl(ifc.cond, True, childCtx)
        elIfs = []
        if cls.VHDL_VER < VhdlVersion.v2008:
            ifTrue = ternaryOpsToIf(ifc.ifTrue)
            ifFalse = ternaryOpsToIf(ifc.ifFalse)
        else:
            ifTrue = ifc.ifTrue
            ifFalse = ifc.ifFalse

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
        def asHdl(statements):
            return [cls.asHdl(s, ctx) for s in statements]

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
    def sensitivityListItem(cls, item, ctx):
        if isinstance(item, Operator):
            item = item.ops[0]
        return cls.asHdl(item, ctx)

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

        sensitivityList = sorted(map(lambda s: cls.sensitivityListItem(s, None), proc.sensitivityList))

        if hasToBeVhdlProcess:
            childCtx = ctx.withIndent()
        else:
            childCtx = copy(ctx)
        
        def createTmpVarFn(suggestedName, dtype):
            # [TODO] it is better to use RtlSignal
            s = SignalItem(None, dtype, virtualOnly=True)
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
            a = Assignment(s.defaultVal, s, virtualOnly=True)
            extraVarsInit.append(cls.Assignment(a, childCtx))

        _hasToBeVhdlProcess = hasToBeVhdlProcess
        hasToBeVhdlProcess = extraVars or hasToBeVhdlProcess

        if hasToBeVhdlProcess and not _hasToBeVhdlProcess:
            # add indent because we did not added it before because we did not know t
            oneIndent = getIndent(1)
            statemets = list(map(lambda x: oneIndent + x, statemets))

        return cls.processTmpl.render(
            indent=getIndent(ctx.indent),
            name=proc.name,
            hasToBeVhdlProcess=hasToBeVhdlProcess,
            extraVars=extraVarsSerialized,
            sensitivityList=", ".join(sensitivityList),
            statements=extraVarsInit + statemets
            )

