
class HdlSimConfig():
        
    def beforeSim(self, simulator, signals):
        pass
    
    def logChange(self, nowTime, sig, nextVal):
        "%d: %s <= %s" % (nowTime, sig.name, str(nextVal))
        
    def logPropagation(self, x):
        pass
        #print(x)