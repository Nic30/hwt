import itertools
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps

class FunctionContainer(list):
    """
    Hdl container for functions with same name to support function overloading
    """
    def __init__(self, name, parent):
        super(FunctionContainer, self).__init__()
        self.name = name
        self.parent = parent
    
    def __hash__(self):
        return hash((id(self), self.name))
        
    def append(self, fn, suppressRedefinition=False):
        """
        Append function definition
        """
        if self:
            assert self[0].name == fn.name  # assert every appended function has same name
        if not suppressRedefinition:
            for _fn in self:  # check if same definition exists
                same = True
                for _p, p in itertools.zip_longest(_fn.params, fn.params):
                    if _p._dtype != p._dtype:
                        same = False
                        break
                assert not same

        return list.append(self, fn)

    def lookup(self, *args):
        """
        lookup function definition by args
        this is called on body (f.e. function implementation vhdl package body)
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
    
    def call(self, *args):
        # this is called on header
        body = self.parent.body[self.name]
        
        fn = body.lookup(*args)
        return Operator.withRes(AllOps.CALL, [fn, *args], fn.returnT)
        
    def staticEval(self):
        # function id does not have to be evalueated
        pass
    
