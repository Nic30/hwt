
class HdlSimConfig():
        
    def beforeSim(self, simulator, signals):
        pass
    
    def logChange(self, nowTime, sig, nextVal):
        pass
        #"%d: %s <= %s" % (nowTime, sig.name, str(nextVal))
        
    def logPropagation(self, x):
        pass

    def logApplyingValues(self, simulator, values):
        pass