import itertools


class FnContainer(list):
    """
    Used as container for functions with same name to support function overloading
    """
    def __init__(self, name):
        super(FnContainer, self).__init__()
        self.name = name
        
    def append(self, fn, suppressRedefinition=False):
        if self:
            assert(self[0].name == fn.name)  # assert every appended function has same name
        if not suppressRedefinition:
            for _fn in self:  # check if same definition exists
                same = True
                for _p, p in itertools.zip_longest(_fn.params, fn.params):
                    if _p.dtype != p.dtype:
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
            for _p, p in itertools.zip_longest(args, fn.args):
                if _p.dtype != p.dtype:
                    same = False
                    break
            if same:
                return fn


class Function():
    def __init__(self, name, returnT, params, exprList, isOperator=False):
        """
        class to store hdl function

        @param name: name of the function
        @param returnT: return type
        @param params: list of argument signals
        @param exprList: list of expressions in body
        @param isOperator: is operator flag
        """
        self.name = name
        self.returnT = returnT
        self.params = params
        self.exprList = exprList
        self.isOperator = isOperator
