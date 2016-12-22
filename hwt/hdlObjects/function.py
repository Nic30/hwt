from hwt.hdlObjects.statements import ReturnCalled

class Function():
    """
    Container for hdl cunction
    """
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
            a.updateTime = 0
            p._val = a
        
        try:
            for s in self.exprList:
                s.seqEval()
        except ReturnCalled as r:
            return r.val
        return None
    
    def staticEval(self):
        return self