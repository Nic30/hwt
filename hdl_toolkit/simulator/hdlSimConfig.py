
class HdlSimConfig():
        
    def beforeSim(self, simulator):
        pass
    
    def logChange(self, nowTime, sig, nextVal):
        "%d: %s <= %s" % (nowTime, sig.name, str(nextVal))
        
    def logPropagation(self, x):
        pass
        #print(x)