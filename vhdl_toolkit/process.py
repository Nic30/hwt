from vhdl_toolkit.expr import Assignment
from vhdl_toolkit.templates import VHDLTemplates


class HWProcess():
    overloadedMethods = ['write', 'init', 'read', 'readResp', 'writeAccept']
    def __init__(self, name):
        self.name = name.replace("__", "_")
        self.interfaces = {}
        self.bodyBuff = []
        self.sensitivityList = set()
    def logToProcWrap(self, func):
        def fnWithLogToProc(*args, **kwargs):
            cmdstr = func(*args, **kwargs)
            if isinstance(cmdstr, str):
                self.bodyBuff.append(cmdstr)
            else:
                self.bodyBuff.extend(cmdstr)
                    
            return cmdstr
        return fnWithLogToProc
    
    def register(self, interf):
        if interf.name in self.interfaces.keys():
            raise Exception("This process already constains this interface %s" % interf.name) 
        self.interfaces[interf.name] = interf
        for attr in self.overloadedMethods:
            if hasattr(interf, attr):
                ovrld = self.logToProcWrap(getattr(interf, attr))
                setattr(interf, attr, ovrld)
    
    def sigAssign(self, sig, item):
        self.bodyBuff.append(str(Assignment(sig, item)))
        
    def delay(self, clkCnt):
        self.bodyBuff.append("wait for clk_period * %d;" % (clkCnt))
    
    def __str__(self):
        hasCondition = not(len(self.bodyBuff) == 1 and self.bodyBuff[0].cond == set())
        return VHDLTemplates.process.render({"name": self.name,
                                             "hasCondition": hasCondition,
              "sensitivityList": ", ".join(self.sensitivityList),
              "statements": [ str(s) for s in self.bodyBuff] })
