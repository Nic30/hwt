from hdl_toolkit.hdlObjects.value import Value
from copy import deepcopy


class IntfValueCont(Value):
    def __init__(self, intf):
        self._interface = intf
        self._interfaces = []
        
    def __repr__(self):
        return "<IntfValueCont intf:%s>" % (str(self._interface))
    
    
    def __deepcopy__(self, memo):
        v = IntfValueCont(self._interface)
        for i in self._interfaces:
            v._interfaces.append(i)
            n = i._name
            a = getattr(self, n)
            setattr(v, n, deepcopy(a))
        return v
    
    def __eq__(self, other):
        assert(isinstance(other, IntfValueCont))
        for i in self._interfaces:
            _a = getattr(self, i._name)
            _b = getattr(other, i._name)
            if _a != _b:
                return False
        return True
        