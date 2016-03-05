from vhdl_toolkit.synthetisator.param import getParam

class Literal():
    def __init__(self, _id=None, val=None):
        self.id = _id
        self.val = val
        assert(bool(id) != bool(val))
        if id:
            self.eval = lambda self : id.get()
        else:
            self.eval = lambda self : self.val
            
    @staticmethod
    def get(lit):
        if hasattr(lit, "__call__"):  # is param
            return Literal.get(lit())
        else:
            return getParam(lit)