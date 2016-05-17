from hdl_toolkit.hdlObjects.types import HdlType, InvalidVHDLTypeExc
from hdl_toolkit.synthetisator.templates import VHDLTemplates
from hdl_toolkit.synthetisator.rtlLevel.signal import Signal
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.assignment import Assignment 
from hdl_toolkit.hdlObjects.specialValues import Unconstrained
from hdl_toolkit.synthetisator.rtlLevel.codeOp import IfContainer
from hdl_toolkit.synthetisator.assigRenderer import renderIfTree
from python_toolkit.arrayQuery import arr_any
from hdl_toolkit.synthetisator.param import getParam
from hdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
from hdl_toolkit.synthetisator.exceptions import SerializerException
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.typeDefs import Enum
from hdl_toolkit.hdlObjects.portConnection import PortConnection

# keep in mind that there is no such a thing in vhdl itself
opPrecedence = {AllOps.NOT : 2,
                AllOps.EVENT: 1,
                AllOps.RISING_EDGE: 1,
                AllOps.DIV: 3,
                AllOps.PLUS : 3,
                AllOps.MINUS: 3,
                AllOps.MUL: 3,
                AllOps.MUL: 3,
                AllOps.XOR: 2,
                AllOps.EQ: 2,
                AllOps.NEQ: 2,
                AllOps.AND_LOG: 2,
                AllOps.OR_LOG: 2,
                AllOps.DOWNTO: 2,
                AllOps.GREATERTHAN: 2,
                AllOps.LOWERTHAN: 2,
                AllOps.CONCAT: 2,
                AllOps.INDEX: 1,
                AllOps.TERNARY: 1,
                AllOps.CALL: 1,
                }

class VhdlSerializer():
    
    @classmethod
    def asHdl(cls, obj):
        if hasattr(obj, "asVhdl"):
            return obj.asVhdl(cls)
        elif isinstance(obj, UnitFromHdl):
            return str(obj)
        elif isinstance(obj, Signal):
            return cls.SignalItem(obj)
        elif isinstance(obj, Value):
            return cls.Value(obj)
        else:
            try:
                serFn = getattr(cls, obj.__class__.__name__)
            except AttributeError:
                raise NotImplementedError("Not implemented for %s" % (repr(obj)))
            return serFn(obj)
    
    @classmethod
    def FnContainer(cls, fn):
        return  fn.name
    
    @classmethod
    def Architecture(cls, arch):
        variables = []
        procs = []
        extraTypes = set()
        for v in sorted(arch.variables, key=lambda x: x.name):
            variables.append(cls.SignalItem(v, declaration=True))
            if isinstance(v.dtype, Enum):
                extraTypes.add(v.dtype)
            
        for p in sorted(arch.processes, key=lambda x: x.name):
            procs.append(cls.HWProcess(p))
            
             
        return VHDLTemplates.architecture.render({
        "entityName"         :arch.entityName,
        "name"               :arch.name,
        "variables"          :variables,
        "extraTypes"         :map(lambda typ: cls.VHDLType(typ, declaration=True), extraTypes),
        "processes"          :procs,
        "components"         :arch.components,
        "componentInstances" :arch.componentInstances
        })
   
    @classmethod
    def Assignment(cls, a):
        if a.dst.dtype == a.src.dtype:
            return "%s <= %s" % (cls.asHdl(a.dst), cls.Value(a.src))
        else:
            raise SerializerException("%s <= %s  is not valid assignment because types are different(%s; %s) " % 
                             (cls.asHdl(a.dst), cls.Value(a.src), repr(a.dst.dtype), repr(a.src.dtype)))
    @classmethod
    def comment(cls, comentStr):
        return "--" + comentStr.replace("\n", "\n--")
    
    @classmethod
    def Component(cls, c):
        return VHDLTemplates.component.render({
                "ports": [cls.PortItem(pi) for pi in c.entity.ports],
                "generics": [cls.GenericItem(g) for g in c.entity.generics],
                "entity": c.entity
                })      

    @classmethod
    def ComponentInstance(cls, ci):
        if len(ci.portMaps) == 0 and len(ci.genericMaps) == 0:
            raise Exception("Incomplete component instance")
        return VHDLTemplates.componentInstance.render({
                "name" : ci.name,
                "component": ci.component,
                "portMaps": [cls.PortConnection(x) for x in   ci.portMaps],
                "genericMaps" : [cls.MapExpr(x) for x in   ci.genericMaps]
                })     

    @classmethod
    def Entity(cls, ent):
        ent.ports.sort(key=lambda x: x.name)
        ent.generics.sort(key=lambda x: x.name)

        doc = ent.__doc__
        if doc:
            doc = cls.comment(doc) + "\n"

        entVhdl = VHDLTemplates.entity.render({
                "name": ent.name,
                "ports" : [cls.PortItem(pi) for pi in ent.ports ],
                "generics" : [cls.GenericItem(g) for g in ent.generics]
                })
        if doc:
            return doc + entVhdl   
        else:
            return entVhdl
    
    @classmethod
    def IfContainer(cls, ifc):
        cond = list(ifc.cond)
        if len(cond) == 1:
            cond = cls.asHdl(cond[0])
        else:
            cond = " AND ".join(map(cls.asHdl, cond))  
        return VHDLTemplates.If.render(cond=cond,
                                       ifTrue=ifc.ifTrue,
                                       ifFalse=ifc.ifFalse)  
  
    @classmethod
    def GenericItem(cls, g):
        s = "%s : %s" % (g.name, cls.VHDLType(g.dtype))
        if g.defaultVal is None:
            return s
        else:  
            return  "%s := %s" % (s, cls.Value(getParam(g.defaultVal)))
    
    @classmethod
    def isStaticExpression(cls, sig):
        if isinstance(sig, Value):
            return True
        ds = len(sig.drivers)
        if ds == 1:
            d = sig.singleDriver()
            if isinstance(d, Operator):
                return True
            elif isinstance(d, Assignment):
                if d.dst is sig and len(sig.endpoints) == 1:
                    ep = list(sig.endpoints)[0]
                    if isinstance(ep, Operator) and ep.operator == AllOps.INDEX:
                        return True
                # for o in d.ops:
                #    if not cls.isStaticExpression(o):
                #        return False
                # return True
        elif len(sig.endpoints) == 1:
            e = sig.endpoints[0]
            if isinstance(e, Operator) and e.operator == AllOps.INDEX:
                return True
            
            
                    
        if sig.name.startswith("sig_1"):
            print("")
        return False
            
            
    @classmethod
    def isSignalHiddenInExpr(cls, sig):
        """Some signals are just only conections in expression they done need to be rendered because
        they are hidden inside expression for example sig. from a+b in a+b+c"""
        return cls.isStaticExpression(sig)
        # if len(sig.drivers) == 1:
        #    if len(sig.endpoints) <= 1:
        #        d = list(iter(sig.drivers))[0]
        #        return not isinstance(d, Assignment) \
        #               and not isinstance(d, PortConnection) \
        #               and d.result == sig
        #    else:
        #        for e in sig.endpoints:
        #            if not isinstance(e, Assignment):
        #                return False
        #            if sig is e.src:
        #                return False
        #        return True
        #            
        # else:
        #    return False
    
    @classmethod
    def PortConnection(cls, pc):
        if pc.portItem.dtype != pc.sig.dtype:
            raise SerializerException("Port map %s is nod valid (types does not match)" % (
                      " %s => %s" % (pc.portItem.name, cls.asHdl(pc.sig))))
        return " %s => %s" % (pc.portItem.name, cls.asHdl(pc.sig))      
    
    @classmethod
    def PortItem(cls, pi):
        try:
            return "%s : %s %s" % (pi.name, pi.direction,
                                   cls.VHDLType(pi.dtype))
        except InvalidVHDLTypeExc as e:
            e.variable = pi
            raise e

    @staticmethod
    def BitString_binary(v, width, vldMask=None):
        buff = []
        for i in range(width - 1, -1, -1):
            mask = (1 << i)
            b = v & mask
            
            if vldMask & mask:
                s = "1" if b else "0"
            else:
                s = "X"
            buff.append(s)
        return '"%s"' % (''.join(buff))

    @classmethod
    def BitString(cls, v, width, vldMask=None):
        if vldMask is None:
            vldMask = width
        # if can be in hex
        if width % 4 == 0 and vldMask == (1 << width) - 1:
            return ('X"%0' + str(width // 4) + 'x"') % (v)
        else:  # else in binary
            return cls.BitString_binary(v, width, vldMask)
    
    @classmethod
    def SignalItem(cls, si, declaration=False):
        if declaration:
            if si.isConstant:
                prefix = "CONSTANT"
            else:
                prefix = "SIGNAL"

            s = prefix + " %s : %s" % (si.name, cls.VHDLType(si.dtype))
            if si.defaultVal is not None and si.defaultVal.vldMask:
                return s + " := %s" % cls.Value(si.defaultVal)
            else:
                return s 
        else:
            if cls.isSignalHiddenInExpr(si):
                if not hasattr(si, "origin"):
                    raise Exception("Signal missing origin, there is unconnected signal %s" % (si.name))
                return cls.asHdl(si.origin)
            else:
                return si.name

    @staticmethod
    def VHDLExtraType(exTyp):
        return "TYPE %s IS (%s);" % (exTyp.name, ", ".join(exTyp.values))
    
    @classmethod
    def VHDLGeneric(cls, g):
        t = cls.VHDLType(g.dtype)
        if hasattr(g, "defaultVal"):
            return "%s : %s := %s" % (g.name, t,
                                      cls.Value(g, g.defaultVal))
        else:
            return "%s : %s" % (g.name, t)

    @classmethod
    def VHDLType(cls, typ, declaration=False):
        assert(isinstance(typ, HdlType))
        buff = []
        if declaration:
            if isinstance(typ, Enum):
                buff.extend(["TYPE ", typ.name.upper(), ' IS ('])
                buff.append(", ".join(typ._allValues))
                buff.append(")")
            else:
                raise NotImplementedError("type declaration is not impleneted for type %s" % 
                                          (typ.name))
        else:    
            buff.append(typ.name.upper())
            if typ.constrain is not None and not isinstance(typ.constrain, Unconstrained):
                buff.append("(%s)" % cls.Value(typ.constrain))        
        return "".join(buff)
                
    @classmethod
    def VHDLVariable(cls, v):
        if v.isShared :
            prefix = "SHARED VARIABLE"
        else:
            prefix = "VARIABLE"
        s = prefix + " %s : %s" % (v.name, cls.VHDLType(v.dtype))
        if v.defaultVal is not None:
            return s + " := %s" % cls.Value(v, v.defaultVal)
        else:
            return s 
                
    @classmethod
    def HWProcess(cls, proc):
        body = [s for s in renderIfTree(proc.bodyBuff)]
        hasCondition = arr_any(body, lambda x: isinstance(x, IfContainer))
        return VHDLTemplates.process.render({
              "name": proc.name,
              "hasCond": hasCondition,
              "sensitivityList": ", ".join(proc.sensitivityList),
              "statements": [ cls.asHdl(s) for s in body] })
    
    @classmethod
    def MapExpr(cls, m):
        return   "%s => %s" % (m.compSig.name, cls.asHdl(m.value))
    
    @classmethod
    def Value(cls, val):
        """ 
        @param dst: is VHDLvariable connected with value 
        @param val: value object, can be instance of Signal or Value    """
        if isinstance(val, Value):
            return val.dtype.valAsVhdl(val, cls)
        elif isinstance(val, Signal):
            return cls.SignalItem(val)
        else:
            raise Exception("value2vhdlformat can not resolve value serialization for %s" % (repr(val))) 

    @classmethod
    def Operator(cls, op):
        def p(operand):
            if cls.asHdl(operand).startswith("sig_1"):
                print()
            s = cls.asHdl(operand)
            if isinstance(operand, Signal):
                try:
                    o = operand.singleDriver()
                    if opPrecedence[o.operator] <= opPrecedence[op.operator]:
                        return " (%s) " % s
                except Exception:
                    pass
            return " %s " % s
        
        ops = op.ops
        o = op.operator
        def _bin(name):
            return (" " + name + " ").join(map(lambda x: x.strip(), map(p, ops)))
        
        if o == AllOps.AND_LOG:
            return _bin('AND')
        elif o == AllOps.CALL:
            return "%s(%s)" % (cls.FnContainer(ops[0]), ", ".join(map(p, ops[1:])))
        elif o == AllOps.CONCAT:
            return _bin('&')
        elif o == AllOps.DIV:
            return _bin('/')
        elif o == AllOps.DOWNTO:
            return _bin('DOWNTO')
        elif o == AllOps.EQ:
            return _bin('=')
        elif o == AllOps.EVENT:
            assert(len(ops) == 1)
            return p(ops[0]) + "'EVENT"
        elif o == AllOps.GREATERTHAN:
            return _bin('>')
        elif o == AllOps.INDEX:
            assert(len(ops) == 2)
            return "%s(%s)" % ((p(ops[0])).strip(), p(ops[1]))
        elif o == AllOps.LOWERTHAN:
            return _bin('<')
        elif o == AllOps.MINUS:
            return _bin('-')
        elif o == AllOps.MUL:
            return _bin('*')
        elif o == AllOps.NEQ:
            return _bin('/=')
        elif o == AllOps.NOT:
            assert(len(ops) == 1)
            return "NOT " + p(ops[0])
        elif o == AllOps.OR_LOG:
            return _bin('OR')
        elif o == AllOps.PLUS:
            return _bin('+')
        elif o == AllOps.TERNARY:
            return p(ops[1]) + " WHEN " + p(ops[0]) + " ELSE " + p(ops[2])
        elif o == AllOps.RISING_EDGE:
            assert(len(ops) == 1)
            return "RISING_EDGE(" + p(ops[0]) + ")"
        else:
            raise NotImplementedError("Do not know how to convert %s to vhdl" % (o))
        #     
        # if isinstance(self.strOperator, str):
        #    return  self.strOperator.join(map(p, operator.ops))
        # else:
        #    return self.strOperator(operator, list(map(p, operator.ops)))
