
from functools import wraps
import sys

from hwt.hdlObjects.types.defs import BIT
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.hdlObjects.types.enum import Enum


def dumpMethod(func):
    """decorator which takes functions return and write it as line to dumpFile"""
    @wraps(func)
    def wrapped(*args, **kwrds):
        s = func(*args, **kwrds)
        if s is not None:
            self = args[0]
            self.dumpFile.write(s)
            self.dumpFile.write('\n')
    
    return wrapped

class VcdVarInfo():
    """Info about signal registered in vcd"""
    def __init__(self, _id, dtype):
        if isinstance(dtype, Enum):
            self.width = 1
        else:
            self.width = dtype.bit_length()
        self.id = _id
        self._dtype = dtype

class VcdVarContext(dict):
    """Map of signals registered in this unit"""
    def __init__(self):
        super().__init__()
        self.nextId = 0
        self.idChars = [ chr(i) for i in range(ord("!"), ord("~") + 2) ]
        self.idCharsCnt = len(self.idChars)
        
    def idToStr(self, x):
        if x < 0: sign = -1
        elif x == 0: return self.idChars[0]
        else: sign = 1
        x *= sign
        digits = []
        while x:
            digits.append(self.idChars[x % self.idCharsCnt])
            x //= self.idCharsCnt
        if sign < 0:
            digits.append('-')
        digits.reverse()
        return ''.join(digits)
    
    def register(self, var):
        var_id = self.idToStr(self.nextId)
        if var in self:
            raise KeyError("%s is already registered" % (repr(var)))
        vInf = VcdVarInfo(var_id, var._dtype)
        self[var] = vInf 
        self.nextId += 1
        return vInf
    
class VcdModule():
    """Vcd module - container for variables"""
    def __init__(self, dumpFile, _vars, name):
        self.name = name
        self.dumpFile = dumpFile
        self.vars = _vars
    
    def __enter__(self):
        self.header()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.footer()
        
    @dumpMethod
    def header(self):
        return "$scope module %s $end" % self.name


    @dumpMethod    
    def var(self, sig):
        vInf = self.vars.register(sig)
        if isinstance(vInf._dtype, Enum):
            sigType = 'real'
        else:    
            sigType = 'wire'
            
        return "$var %s %d %s %s $end" % (sigType, vInf.width, vInf.id, sig.name)
     
    @dumpMethod
    def footer(self):
        return "$upscope $end"

class VcdWritter():
    def __init__(self, dumpFile=sys.stdout):
        self.dumpFile = dumpFile
        self.vars = VcdVarContext()
        self.lastTime = -1
        self.defaultTop = None 
    
    @dumpMethod
    def date(self, text):
        return "$date\n   %s\n$end" % text
    
    @dumpMethod
    def version(self, text):
        return "$version   \n%s\n$end" % text
    
    @dumpMethod
    def timescale(self, picoSeconds):
        return "$timescale %dps $end" % picoSeconds
    
    def module(self, name):
        return VcdModule(self.dumpFile, self.vars, name)
    
    @dumpMethod
    def enddefinitions(self):
        return "$enddefinitions $end"
    
    @dumpMethod
    def setTime(self, t):
        lt = self.lastTime
        if  lt == t:
            return
        elif lt < t:
            self.lastTime = t
            return "#%d" % (t)
        else:
            raise Exception("VcdWritter invalid time update %d -> %d" % (lt, t))
        
    
    @dumpMethod
    def change(self, time, sig, newVal):
        self.setTime(time)
        varInfo = self.vars[sig]
        if isinstance(sig._dtype, Enum):
            if newVal.vldMask:
                val = newVal.val
            else:
                val = "XXXX"
            frmt = "s%s %s"
        else:
            val = VhdlSerializer.BitString_binary(newVal.val, varInfo.width, newVal.vldMask)
            val = val.replace('"', "")
             
            if varInfo._dtype == BIT:
                frmt = "%s%s"
            else:
                frmt = "b%s %s" 
            
        return frmt % (val, varInfo.id)
    
    
    
