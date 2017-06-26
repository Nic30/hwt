from hwt.hdlObjects.assignment import Assignment
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.statements import IfContainer
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.sliceVal import SliceVal
from hwt.hdlObjects.variables import SignalItem
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.vhdl.utils import VhdlVersion, vhdlTmplEnv
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hwt.serializer.serializerClases.indent import getIndent


IfTmpl = vhdlTmplEnv.get_template('if.vhd')
SwitchTmpl = vhdlTmplEnv.get_template('switch.vhd')


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
    def WaitStm(cls, w, createTmpVarFn, indent=0):
        indent_str = getIndent(indent)

        if w.isTimeWait:
            return "%swait for %d ns" % (indent_str, w.waitForWhat)
        elif w.waitForWhat is None:
            return "%swait" % indent_str
        else:
            raise NotImplementedError()

    @classmethod
    def Assignment(cls, a, createTmpVarFn, indent=0):
        dst = a.dst
        assert isinstance(dst, SignalItem)

        def asHdl(obj):
            return cls.asHdl(obj, createTmpVarFn)

        def valAsHdl(v):
            return cls.Value(v, createTmpVarFn)

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

        indent_str = getIndent(indent)
        dstStr = asHdl(dst)
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
    def IfContainer(cls, ifc, createTmpVarFn, indent=0):
        def asHdl(obj):
            return cls.asHdl(obj, createTmpVarFn, indent=indent + 1)

        cond = cls.condAsHdl(ifc.cond, True, createTmpVarFn)
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

            elIfs.append((cls.condAsHdl(c, True, createTmpVarFn), [asHdl(s) for s in statements]))

        return IfTmpl.render(
                            indent=getIndent(indent),
                            cond=cond,
                            ifTrue=[asHdl(s) for s in ifTrue],
                            elIfs=elIfs,
                            ifFalse=[asHdl(s) for s in ifFalse])

    @classmethod
    def SwitchContainer(cls, sw, createTmpVarFn, indent=0):
        def asHdl(obj):
            return cls.asHdl(obj, createTmpVarFn, indent=indent + 1)
        switchOn = cls.condAsHdl(sw.switchOn, False, createTmpVarFn)

        cases = []
        for key, statements in sw.cases:
            key = cls.asHdl(key, createTmpVarFn)

            if cls.VHDL_VER < VhdlVersion.v2008:
                statements = ternaryOpsToIf(statements)

            cases.append((key, [asHdl(s) for s in statements]))

        if sw.default:
            cases.append((None, [asHdl(s) for s in sw.default]))

        return SwitchTmpl.render(
                            indent=getIndent(indent),
                            switchOn=switchOn,
                            cases=cases)

    @classmethod
    def MapExpr(cls, m, createTmpVar):
        return "%s => %s" % (m.compSig.name, cls.asHdl(m.value, createTmpVar))
