from hdl_toolkit.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hdl_toolkit.hdlObjects.operatorDefs import AllOps

opPrecedence = {AllOps.NOT : 4,
                AllOps.EVENT: 1,
                AllOps.RISING_EDGE: 1,
                AllOps.DIV: 4,
                AllOps.ADD : 5,
                AllOps.SUB: 5,
                AllOps.MUL: 4,
                AllOps.XOR: 9,
                AllOps.EQ: 10,
                AllOps.NEQ: 10,
                AllOps.AND_LOG: 10,
                AllOps.OR_LOG: 10,
                AllOps.DOWNTO: 1,
                AllOps.GREATERTHAN: 10,
                AllOps.LOWERTHAN: 10,
                AllOps.CONCAT: 1,
                AllOps.INDEX: 1,
                AllOps.TERNARY: 1,
                AllOps.CALL: 1,
                }

class SimModelSerializer_ops():
    @classmethod
    def BitToBool(cls, cast):
        v = 0 if cast.sig.negated else 1
        return cls.asHdl(cast.sig) + "._eq(hBit(%d))" % v

    @classmethod
    def Operator(cls, op):
        def p(operand):
            s = cls.asHdl(operand)
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
            return _bin('&')
        elif o == AllOps.OR_LOG:
            return _bin('|')
        elif o == AllOps.XOR:
            return _bin('^')
        elif o == AllOps.NOT:
            assert len(ops) == 1
            return "~" + p(ops[0])
        elif o == AllOps.CALL:
            return "%s(%s)" % (cls.FunctionContainer(ops[0]), ", ".join(map(p, ops[1:])))
        elif o == AllOps.CONCAT:
            return "Concat(%s, %s)" % (p(ops[0]), p(ops[1]))
        elif o == AllOps.DIV:
            return _bin('//')
        elif o == AllOps.DOWNTO:
            return "SliceVal((%s, %s), SLICE, True)" % (p(ops[0]), p(ops[1]))
        elif o == AllOps.EQ:
            return '(%s)._eq(%s)' % (p(ops[0]), p(ops[1]))
        elif o == AllOps.EVENT:
            assert len(ops) == 1
            return p(ops[0]) + "._hasEvent(sim)"
        elif o == AllOps.GREATERTHAN:
            return _bin('>')
        elif o == AllOps.GE:
            return _bin('>=')
        elif o == AllOps.LE:
            return _bin('<=')
        elif o == AllOps.INDEX:
            assert len(ops) == 2
            return "%s[%s]" % ((cls.asHdl(ops[0])).strip(), p(ops[1]))
        elif o == AllOps.LOWERTHAN:
            return _bin('<')
        elif o == AllOps.SUB:
            return _bin('-')
        elif o == AllOps.MUL:
            return _bin('*')
        elif o == AllOps.NEQ:
            return _bin('!=')
        elif o == AllOps.ADD:
            return _bin('+')
        elif o == AllOps.TERNARY:
            return "(%s)._ternary(%s, %s)" % tuple(map(cls.asHdl, ops)) 
        elif o == AllOps.RISING_EDGE:
            assert len(ops) == 1
            return "(%s)._onRisingEdge(sim.now)" % (p(ops[0]))
        elif o == AllOps.FALLIGN_EDGE:
            assert len(ops) == 1
            return "(%s)._onFallingEdge(sim.now)" % (p(ops[0]))
        elif o == AllOps.BitsAsSigned:
            assert len(ops) == 1
            return  "(%s)._signed()" % p(ops[0])
        elif o == AllOps.BitsAsUnsigned:
            assert len(ops) == 1
            return  "(%s)._unsigned()" % p(ops[0])
        elif o == AllOps.BitsAsVec:
            assert len(ops) == 1
            return  "(%s)._vec()" % p(ops[0])
        elif o == AllOps.BitsToInt:
            assert len(ops) == 1
            op = ops[0]
            return "convertBits(%s, %s, INT)" % (cls.HdlType_bits(op._dtype), cls.asHdl(op))
        elif o == AllOps.IntToBits:
            assert len(ops) == 1
            resT = op.result._dtype
            return "convertInteger(%s, %s, %s)" % (cls.HdlType(ops[0]._dtype),
                                                   cls.asHdl(ops[0]),
                                                   cls.HdlType_bits(resT))
            
        elif o == AllOps.POW:
            assert len(ops) == 2
            return  "pow(%s, %s)" % (p(ops[0]), p(ops[1]))
        else:
            raise NotImplementedError("Do not know how to convert %s to simModel" % (o))
