from hwt.hdl.value import Value
from hwt.pyUtils.arrayQuery import arr_all
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal, RtlSignalBase


def getCtxFromOps(operands):
    for o in operands:
        if isinstance(o, RtlSignalBase):
            return o.ctx
    raise TypeError("Can not find context because there is no signal in ops"
                    "(value operators should be already resolved)")


def isConst(item):
    return isinstance(item, Value) or item._const


class Operator():
    """
    Class of operator in expression tree

    :ivar operands: list of operands
    :ivar evalFn: function to evaluate this operator
    :ivar operator: OpDefinition instance
    :ivar result: result signal of this operator
    """

    def __init__(self, operator, operands):
        self.operands = list(operands)
        self.operator = operator
        self.result = None

    def registerSignals(self, outputs=[]):
        """
        Register potential signals to drivers/endpoints
        """
        for o in self.operands:
            if isinstance(o, RtlSignalBase):
                if o in outputs:
                    o.drivers.append(self)
                else:
                    o.endpoints.append(self)
            elif isinstance(o, Value):
                pass
            else:
                raise NotImplementedError(
                    "Operator operands can be"
                    " only signal or values got:%r" % (o))

    def staticEval(self):
        """
        Recursively statistically evaluate result of this operator
        """
        for o in self.operands:
            o.staticEval()
        self.result._val = self.evalFn()

    def evalFn(self, simulator=None):
        """
        Syntax sugar
        """
        return self.operator.eval(self, simulator=simulator)

    def __eq__(self, other):
        return self is other or (
            type(self) is type(other) and
            self.operator == other.operator and
            self.operands == other.operands
        )

    @staticmethod
    def withRes(opDef, operands, resT, outputs=[]):
        """
        Create operator with result signal

        :ivar resT: data type of result signal
        :ivar outputs: iterable of singnals which are outputs
            from this operator
        """
        op = Operator(opDef, operands)
        out = RtlSignal(getCtxFromOps(operands), None, resT)
        out._const = arr_all(op.operands, isConst)
        out.drivers.append(op)
        out.origin = op
        op.result = out
        op.registerSignals(outputs)
        if out._const:
            out.staticEval()
        return out

    def __hash__(self):
        return hash((self.operator, frozenset(self.operands)))

    def __repr__(self):
        return "<%s operator:%r, operands:%r>" % (self.__class__.__name__,
                                                  self.operator,
                                                  self.operands)
