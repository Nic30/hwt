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
                                      [Assignment(d.ops[1], st.dst)]
                                      ,
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
    def WaitStm(cls, w, createTmpVarFn):
        if w.isTimeWait:
            return "wait for %d ns" % w.waitForWhat
        elif w.waitForWhat is None:
            return "wait"
        else:
            raise NotImplementedError()

    @classmethod
    def Assignment(cls, a, createTmpVarFn):
        dst = a.dst
        assert isinstance(dst, SignalItem)
        asHdl = lambda obj : cls.asHdl(obj, createTmpVarFn)
        valAsHdl = lambda v: cls.Value(v, createTmpVarFn)
        if dst.virtualOnly:
            symbol = ":="
        else:
            symbol = "<="
        
        if a.indexes is not None:
            for i in a.indexes:
                if isinstance(i, SliceVal):
                    i = i.clone()
                    i.val = (i.val[0] + 1, i.val[1])
                dst = dst[i]   
        
                    
        if dst._dtype == a.src._dtype:
            return "%s %s %s" % (asHdl(dst), symbol, valAsHdl(a.src))
        else:
            srcT = a.src._dtype
            dstT = dst._dtype
            if isinstance(srcT, Bits) and isinstance(dstT, Bits):
                sLen = srcT.bit_length()
                dLen = dstT.bit_length()
                if sLen == dLen:
                    if sLen == 1 and srcT.forceVector != dstT.forceVector:
                        if srcT.forceVector:
                            return "%s %s %s(0)" % (asHdl(dst), symbol, valAsHdl(a.src)) 
                        else:
                            return "%s(0) %s %s" % (asHdl(dst), symbol, valAsHdl(a.src)) 
                    elif srcT.signed is not dstT.signed:
                        return "%s %s %s" % (asHdl(dst), symbol, valAsHdl(a.src._convSign(dstT.signed)))
            
            raise SerializerException("%s %s %s  is not valid assignment\n because types are different (%s; %s) " % 
                         (asHdl(dst), symbol, valAsHdl(a.src), repr(dst._dtype), repr(a.src._dtype)))

    @classmethod
    def IfContainer(cls, ifc, createTmpVarFn):
        asHdl = lambda obj : cls.asHdl(obj, createTmpVarFn)
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
        
        return IfTmpl.render(cond=cond,
                             ifTrue=[asHdl(s) for s in ifTrue],
                             elIfs=elIfs,
                             ifFalse=[asHdl(s) for s in ifFalse])  
    
    @classmethod
    def SwitchContainer(cls, sw, createTmpVarFn):
        asHdl = lambda obj : cls.asHdl(obj, createTmpVarFn)
        switchOn = cls.condAsHdl(sw.switchOn, False, createTmpVarFn)
        
        cases = []
        for key, statements in sw.cases:
            if key is not None:  # None is default
                key = cls.asHdl(key, createTmpVarFn)
                
            if cls.VHDL_VER < VhdlVersion.v2008:
                statements = ternaryOpsToIf(statements)
                
            cases.append((key, [asHdl(s) for s in statements]))  
        return SwitchTmpl.render(switchOn=switchOn,
                                 cases=cases)  
    
    @classmethod
    def MapExpr(cls, m, createTmpVar):
        return   "%s => %s" % (m.compSig.name, cls.asHdl(m.value, createTmpVar))
