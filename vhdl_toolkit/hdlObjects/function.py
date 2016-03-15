import itertools


class FunctionContainer(list):
    """
    Used as container for functions with same name to support function overloading
    """
    def append(self, fn):
        if self:
            assert(self[0].name == fn.name) # assert every appended function has same name
        
        for _fn in self: # check if same definition exists
            same = True
            for _arg, arg in itertools.zip_longest(_fn.args, fn.args):
                if _arg.dtype != arg.dtype:
                    same = False
                    break
            assert(not same)
        
        return list.append(self, fn)

    def lookup(self, args):
        """
        lookup function definition by args
        """
        for fn in self: # check if same definition exists
            same = True
            for _arg, arg in itertools.zip_longest(args, fn.args):
                if _arg.dtype != arg.dtype:
                    same = False
                    break
            if same:
                return fn    
        
class Function():
    def __init__(self, name, returnT, args, exprList, isOperator=False):
        """
        class to store hdl function
        
        @param name: name of the function
        @param returnT: return type
        @param args: list of argument signals
        @param exprList: list of expressions in body
        @param isOperator: is operator flag   
        """        
        self.name = name
        self.returnT = returnT
        self.args = args
        self.exprList = exprList
        self.isOperator = isOperator
