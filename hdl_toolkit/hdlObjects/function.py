import itertools
from hdl_toolkit.synthetisator.rtlLevel.codeOp import ReturnCalled
from hdl_toolkit.hdlObjects.types.integer import Integer

class FnContainer(list):
    """
    Used as container for functions with same name to support function overloading
    """
    def __init__(self, name, parent):
        super(FnContainer, self).__init__()
        self.name = name
        self.parent = parent
    
    def __hash__(self):
        return hash((id(self), self.name))
        
    def append(self, fn, suppressRedefinition=False):
        if self:
            assert(self[0].name == fn.name)  # assert every appended function has same name
        if not suppressRedefinition:
            for _fn in self:  # check if same definition exists
                same = True
                for _p, p in itertools.zip_longest(_fn.params, fn.params):
                    if _p._dtype != p._dtype:
                        same = False
                        break
                assert(not same)

        return list.append(self, fn)

    def lookup(self, args):
        """
        lookup function definition by args
        """
        # check if same definition exists
        for fn in self:
            same = True
            for _p, p in itertools.zip_longest(args, fn.params):
                if _p._dtype != p._dtype and \
                 not (isinstance(_p._dtype, Integer), isinstance(p._dtype, Integer)):
                    same = False
                    break
            if same:
                return fn
        raise KeyError("Function was not found")
    def staticEval(self):
        # function id does not have to be evalueated
        pass
    
class Function():
    def __init__(self, name, returnT, ctx, params, _locals, exprList, isOperator=False):
        """
        class to store hdl function

        @param name: name of the function
        @param returnT: return type
        @param ctx: hdl context of this funtion
        @param params: list of argument signals
        @param _locals : local variables in this function
        @param exprList: list of expressions in body
        @param isOperator: is operator flag
        """
        self.name = name
        self.returnT = returnT
        self.ctx = ctx
        self.params = params
        self.locals = _locals
        self.exprList = exprList
        self.isOperator = isOperator

    def call(self, *args):
        for p, a in zip(self.params, args):
            p._val = a
        
        try:
            for s in self.exprList:
                s.seqEval()
        except ReturnCalled as r:
            return r.val
        return None
