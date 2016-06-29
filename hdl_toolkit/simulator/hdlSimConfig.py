from hdl_toolkit.hdlObjects.assignment import Assignment


class HdlSimConfig():
    def __init__(self):
        # rising faling duration
        self.risFalDur = 100
        self.log = False
    
    
    def propagDelay(self, obj):
        if isinstance(obj, Assignment):
            return 0
        else:
            return 50
    def beforeSim(self, simulator):
        pass
    
    def logChange(self, nowTime, sig, nextVal):
        "%d: %s <= %s" % (nowTime, sig.name, str(nextVal))
        
    def logPropagation(self, x):
        print(x)