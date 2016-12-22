from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdlObjects.operatorDefs import AllOps, OpDefinition


# keep in mind that there is no such a thing in vhdl itself
opPrecedence = {AllOps.NOT : 2,
                AllOps.EVENT: 1,
                AllOps.RISING_EDGE: 1,
                AllOps.DIV: 3,
                AllOps.ADD : 3,
                AllOps.SUB: 3,
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

def isResultOfTypeConversion(sig):
    try:
        d = sig.drivers[0]
    except IndexError:
        return False
    
    if sig.hidden:
        return True
    return False

class VhdlSerializer_ops():

    @classmethod
    def BitToBool(cls, cast):
        v = 0 if cast.sig.negated else 1
        return cls.asHdl(cast.sig) + "=='%d'" % v

    
    @classmethod
    def Operator(cls, op, createTmpVarFn):
        def p(operand):
            s = cls.asHdl(operand, createTmpVarFn)
            if isinstance(operand, RtlSignalBase):
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
        elif o == AllOps.OR_LOG:
            return _bin('OR')
        elif o == AllOps.XOR:
            return _bin('XOR')
        elif o == AllOps.NOT:
            assert len(ops) == 1
            return "NOT " + p(ops[0])
        elif o == AllOps.CALL:
            return "%s(%s)" % (cls.FunctionContainer(ops[0]), ", ".join(map(p, ops[1:])))
        elif o == AllOps.CONCAT:
            return _bin('&')
        elif o == AllOps.DIV:
            return _bin('/')
        elif o == AllOps.DOWNTO:
            return _bin('DOWNTO')
        elif o == AllOps.EQ:
            return _bin('=')
        elif o == AllOps.EVENT:
            assert len(ops) == 1
            return p(ops[0]) + "'EVENT"
        elif o == AllOps.GREATERTHAN:
            return _bin('>')
        elif o == AllOps.GE:
            return _bin('>=')
        elif o == AllOps.LE:
            return _bin('<=')
        elif o == AllOps.INDEX:
            assert len(ops) == 2
            o1 = ops[0]
            if isResultOfTypeConversion(o1):
                o1 = createTmpVarFn("tmpTypeConv", o1._dtype)
                o1.defaultVal = ops[0]
            
            return "%s(%s)" % (cls.asHdl(o1, createTmpVarFn).strip(), p(ops[1]))
        elif o == AllOps.LOWERTHAN:
            return _bin('<')
        elif o == AllOps.SUB:
            return _bin('-')
        elif o == AllOps.MUL:
            return _bin('*')
        elif o == AllOps.NEQ:
            return _bin('/=')
        elif o == AllOps.ADD:
            return _bin('+')
        elif o == AllOps.TERNARY:
            return p(ops[1]) + " WHEN " + cls.condAsHdl([ops[0]], True, createTmpVarFn) + " ELSE " + p(ops[2])
        elif o == AllOps.RISING_EDGE:
            assert len(ops) == 1
            return "RISING_EDGE(" + p(ops[0]) + ")"
        elif o == AllOps.FALLIGN_EDGE:
            assert len(ops) == 1
            return "FALLING_EDGE(" + p(ops[0]) + ")"
        elif o == AllOps.BitsAsSigned:
            assert len(ops) == 1
            return  "SIGNED(" + p(ops[0]) + ")"
        elif o == AllOps.BitsAsUnsigned:
            assert len(ops) == 1
            return  "UNSIGNED(" + p(ops[0]) + ")"
        elif o == AllOps.BitsAsVec:
            assert len(ops) == 1
            return  "STD_LOGIC_VECTOR(" + p(ops[0]) + ")"
        elif o == AllOps.BitsToInt:
            assert len(ops) == 1
            op = cls.asHdl(ops[0], createTmpVarFn)
            if ops[0]._dtype.signed is None:
                op = "UNSIGNED(%s)" % op
            return "TO_INTEGER(%s)" % op
        elif o == AllOps.IntToBits:
            assert len(ops) == 1
            resT = op.result._dtype
            op_str = cls.asHdl(ops[0], createTmpVarFn)
            w = resT.bit_length()
            
            if resT.signed is None:
                return "STD_LOGIC_VECTOR(TO_UNSIGNED(" + op_str + ", %d))" % (w)
            elif resT.signed:
                return "TO_UNSIGNED(" + op_str + ", %d)" % (w)
            else:
                return "TO_UNSIGNED(" + op_str + ", %d)" % (w)
            
        elif o == AllOps.POW:
            assert len(ops) == 2
            return _bin('**')
        else:
            raise NotImplementedError("Do not know how to convert %s to vhdl" % (o))

