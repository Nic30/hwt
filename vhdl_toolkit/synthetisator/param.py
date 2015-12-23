



class Param():
    def __init__(self, initval):
        self.val = initval
        a = 1
        for propName in dir(initval):
            prop = getattr(initval, propName)
            if isinstance(prop, a.__abs__.__class__):
                def wrap(*args, **kwargs):
                    return getattr(self.val, propName)(*args, **kwargs)
                setattr(self, propName, wrap)
    def get(self):
        return  self.val
    def inherieit(self, param):
        self.set(param.get())
    def set(self, val):
        self.val = val
        
        
def getParam(p):
    if isinstance(p,Param):
        return p.get()
    else:
        return p