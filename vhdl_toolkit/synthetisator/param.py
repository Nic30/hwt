



class Param():
    def __init__(self, initval):
        self.val = initval
        self.parent = None
        a = 1
        for propName in dir(initval):
            prop = getattr(initval, propName)
            if isinstance(prop, a.__abs__.__class__):
                def wrap(*args, **kwargs):
                    return getattr(self.val, propName)(*args, **kwargs)
                setattr(self, propName, wrap)
    def get(self):
        if self.parent:
            return self.parent.get()
        else:
            return self.val
        
    def inherieit(self, param):
        self.parent = param
    
    def set(self, val):
        self.val = val
    
    def __str__(self):
        return "<%s, val=%s>" %(str(self.__class__), self.get()) 
        
def getParam(p):
    if isinstance(p,Param):
        return p.get()
    else:
        return p