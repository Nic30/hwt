from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdlObjects.operatorDefs import AllOps

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
        return cls.asHdl(cast.sig) + "._eq__val(hBit(%d))" % v

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
            return "(%s).%s(%s)" % (p(ops[0]).strip(), name, p(ops[1]).strip())
        
        if o == AllOps.AND_LOG:
            return _bin('_and__val')
        elif o == AllOps.OR_LOG:
            return _bin('_or__val')
        elif o == AllOps.XOR:
            return _bin('_xor__val')
        elif o == AllOps.NOT:
            assert len(ops) == 1
            return "(%s)._invert__val()" % p(ops[0])
        # elif o == AllOps.CALL:
        #    return "%s(%s)" % (cls.FunctionContainer(ops[0]), ", ".join(map(p, ops[1:])))
        elif o == AllOps.CONCAT:
            return "(%s)._concat__val(%s)" % (p(ops[0]), p(ops[1]))
        elif o == AllOps.DIV:
            return _bin('_floordiv__val')
        elif o == AllOps.DOWNTO:
            return "SliceVal((%s, %s), SLICE, True)" % (p(ops[0]), p(ops[1]))
        elif o == AllOps.EQ:
            return '(%s)._eq__val(%s)' % (p(ops[0]), p(ops[1]))
        elif o == AllOps.EVENT:
            assert len(ops) == 1
            return p(ops[0]) + "._hasEvent__val(sim)"
        elif o == AllOps.GREATERTHAN:
            return _bin('_gt__val')
        elif o == AllOps.GE:
            return _bin('_ge__val')
        elif o == AllOps.LE:
            return _bin('_le__val')
        elif o == AllOps.INDEX:
            assert len(ops) == 2
            return "(%s)._getitem__val(%s)" % ((cls.asHdl(ops[0])).strip(), p(ops[1]))
        elif o == AllOps.LOWERTHAN:
            return _bin('_lt__val')
        elif o == AllOps.SUB:
            return _bin('_sub__val')
        elif o == AllOps.MUL:
            return _bin('_mul__val')
        elif o == AllOps.NEQ:
            return _bin('_ne__val')
        elif o == AllOps.ADD:
            return _bin('_add__val')
        elif o == AllOps.TERNARY:
            return "(%s)._ternary__val(%s, %s)" % tuple(map(cls.asHdl, ops)) 
        elif o == AllOps.RISING_EDGE:
            assert len(ops) == 1
            return "(%s)._onRisingEdge__val(sim.now)" % (p(ops[0]))
        elif o == AllOps.FALLIGN_EDGE:
            assert len(ops) == 1
            return "(%s)._onFallingEdge__val(sim.now)" % (p(ops[0]))
        elif o == AllOps.BitsAsSigned:
            assert len(ops) == 1
            return  "(%s)._convSign__val(True)" % p(ops[0])
        elif o == AllOps.BitsAsUnsigned:
            assert len(ops) == 1
            return  "(%s)._convSign__val(False)" % p(ops[0])
        elif o == AllOps.BitsAsVec:
            assert len(ops) == 1
            return  "(%s)._convSign__val(None)" % p(ops[0])
        elif o == AllOps.BitsToInt:
            assert len(ops) == 1
            op = ops[0]
            return "convertSimBits__val(%s, %s, SIM_INT)" % (cls.HdlType_bits(op._dtype), cls.asHdl(op))
        elif o == AllOps.IntToBits:
            assert len(ops) == 1
            resT = op.result._dtype
            return "convertSimInteger__val(%s, %s, %s)" % (cls.HdlType(ops[0]._dtype),
                                                   cls.asHdl(ops[0]),
                                                   cls.HdlType_bits(resT))
            
        elif o == AllOps.POW:
            assert len(ops) == 2
            return  "power(%s, %s)" % (p(ops[0]), p(ops[1]))
        else:
            raise NotImplementedError("Do not know how to convert %s to simModel" % (o))
