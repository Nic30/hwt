from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.synthetisator.rtlLevel.signal import Signal
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.synthetisator.rtlLevel.signal.walkers import walkAllOriginSignals

def areInstanceOf(a, b, cls):
    return isinstance(a, cls) and isinstance(b, cls)

class ExprComparator():
    @staticmethod
    def isSimilar(exprA, exprB, diffInA):
        """
        @return:  tuple (match, exprDiffB)
        @attention: works only on simple expressions like constrain definition,
                    does not support multiple drivers for signals
        """
        if exprA  is diffInA:
            return (True, exprB)
        elif areInstanceOf(exprA, exprB, Signal):
            try:
                originA = exprA.origin
                originB = exprB.origin
            except AttributeError:
                return (False, None)
            return ExprComparator.isSimilar(originA, originB, diffInA)
        elif areInstanceOf(exprA, exprB, Operator):
            if exprA.operator == exprB.operator:
                diff = None
                for opA, opB in zip(exprA.ops, exprB.ops):
                    m = ExprComparator.isSimilar(opA, opB, diffInA)
                    if not m[0]:
                        return (False, None)
                    if not m[1] is None:
                        assert(diff is m[1] or diff is None)
                        diff = m[1]
                return (True, diff)
        elif areInstanceOf(exprA, exprB, Value) and exprA._eq(exprB).val:
            return (True, None)
        return (False, None)
    
    @staticmethod    
    def findExprDiffInParam(exprA, exprB):
        params = list(walkAllOriginSignals(exprA))
        l = len(params)
        if l == 0:
            return 
        elif l == 1:
            m = ExprComparator.isSimilar(exprA, exprB, params[0])
            if m[0] and m[1] is not None:
                yield (params[0], m[1])
        else:
            raise NotImplementedError("Searching for multiple differences in expression")

class Map():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
   
    def __str__(self):
        return "%s => %s" % (self.dst.name, self.src.name)  

 
