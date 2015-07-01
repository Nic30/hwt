from vhdl_toolkit.expr import Assigment

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
            self.bodyBuff.append(cmdstr)
            return cmdstr
        return fnWithLogToProc
    
    def register(self, interf):
        if interf.prefix in self.interfaces.keys():
            raise Exception("Redining interface %s" % interf.prefix) 
        self.interfaces[interf.prefix] = interf
        for attr in self.overloadedMethods:
            if hasattr(interf, attr):
                ovrld = self.logToProcWrap(getattr(interf, attr))
                setattr(interf, attr, ovrld)
    
    def sigAssign(self, sig, item):
        self.bodyBuff.append(str(Assigment(sig, item)))
        
    def delay(self, clkCnt):
        self.bodyBuff.append("wait for clk_period * %d;" % (clkCnt))
    
    def __str__(self):
        return """%s: process --(%s)
        begin
           %s
        end process;
        """ % (self.name,
              ", ".join(self.sensitivityList),
              "\n".join([ str(s) for s in self.bodyBuff]))
