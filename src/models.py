import re
from iterators import forBracketBlock, forVhdlBlock

entityReg = re.compile('\s*entity\s+(\S+)\s*', re.IGNORECASE) # start of entity
architectureReg = re.compile('architecture\s+(\S+)\s+of\s+(\S+)\s*', re.IGNORECASE) # architecture start without begin

class BasicVariable(object):
    def __init__(self, name, typ, val):
        self.name = name.lower()
        self.typ = typ.lower()
        self.val = val
    
    def __repr__(self):
        return  "%s %s = %s" % (self.typ, self.name, self.val) 
    
class BaseMap(object):
    def __init__(self, source, target):
        self.source = source.lower()
        self.target = target.lower()
    def __repr__(self):
        return "%s => %s" % (self.source, self.target)
    
#class Function(object):
#    headMatch = re.compile("function\s+.*\s+return\s+(\S+)\s*", re.IGNORECASE)
#    def __init__(self, headMatch, fileName):
#        self.name = headMatch.group(1)
#        self.params = []
#        self.fileName = fileName
    
class Architecture(object):
    def __init__(self, name, entityName, lineGen, filename):
        self.name = name.lower()
        self.entityName = entityName.lower()
        if not self.entityName.startswith("work."):
            self.entityName = "work." + self.entityName.lower()
        self.lineGen = lineGen
        self.portMaps = []
        self.entities = []
        self.filename = filename
        self._parse()
        
    def _parse(self):
        self._readHeader()
        portMapHeadReg = re.compile('\s*(\S*\s*:)\s*entity\s*(\S*)(\(\w*\))?', re.IGNORECASE)
        for line in forVhdlBlock(self.lineGen,1):
            pM = portMapHeadReg.match(line)
            if pM:
                name = pM.group(1).split(":")[0]
                entity = pM.group(2)
                while line != "port map":
                    line = next(self.lineGen)
                p = PortMap(name, entity, self.lineGen)
                self.portMaps.append(p) 
        del(self.lineGen)
    def _readHeader(self):
        architectureBeginReg = re.compile('^\s*begin\s*$', re.IGNORECASE)
        fnReq = re.compile('^\s*function\s+(\w+)', re.IGNORECASE)
        procedReq = re.compile('^\s*procedure\s+(\w+)', re.IGNORECASE)
        mBegin = None
        while not mBegin:
            line = next(self.lineGen)
            fnMatch = fnReq.match(line)
            procedMatch = procedReq.match(line)
            if fnMatch or procedMatch:
                for l in forVhdlBlock(self.lineGen, 0):
                    pass
            else:     
                mBegin = architectureBeginReg.match(line)

    def __repr__(self):
        return "<VHDL.Architecture %s of entity %s, portMaps.len = %d >" % (self.name, self.entityName, len(self.portMaps))

class PortMap(object):
    def __init__(self, name, entityName, lineGen):
        self.name = name.lower()
        self.entityName = entityName.lower().split("(")[0]
        if not self.entityName.startswith("work."):
            self.entityName = "work." + self.entityName.lower()
        self.lineGen = lineGen
        self.maps = []
        self._parse()
        
    def _parse(self):
        mapReg = re.compile('^\s*(\S+)\s*=>\s*([^ ,;]+)\s*,?', re.IGNORECASE)
        for line in forBracketBlock(self.lineGen):
            mm = mapReg.match(line)
            if mm:
                m = BaseMap(mm.group(1), mm.group(2))
                self.maps.append(m)
        del(self.lineGen)      
          
    def __repr__(self):
        return "< name: %s , entity: %s, maps: %s >" % (self.name, self.entityName, self.maps)
        
class Entity(object):
    objInEntityEnd = re.compile('^\s*\)\s*;\s*$', re.IGNORECASE)  # any object in entity (port / generic)
    def __init__(self,name, lineGen, filename):
        """ lineGen is line generator """
        self.name = name.lower()
        if not self.name.startswith("work."):
            self.name = "work." + self.name.lower()
        self.lineGen = lineGen
        self.port = []
        self.generic = []
        self.architectures = []
        self.filename = filename
        self._parse()
        
    def _parse(self):
        portReg = re.compile("^\s*port\s*", re.IGNORECASE) # start of port in entity
        genericReg = re.compile("^\s*generic\s*", re.IGNORECASE) # start of generic in entity
        for line in forVhdlBlock(self.lineGen, 0):
            mGeneric = genericReg.match(line)
            mPort = portReg.match(line)
            if mGeneric:
                self.readGeneric()
            if mPort:
                self.readPort()
        del(self.lineGen)
                
    def readGeneric(self):
        genericRecReg = re.compile('^\s*(\S+)\s*:\s*(\S+)\s*:=\s*(\S+)\s*;?', re.IGNORECASE)# one record in generic with value
        for line in forBracketBlock(self.lineGen):
            m= genericRecReg.match(line)
            if m:
                v = BasicVariable(m.group(1), m.group(2),m.group(3))
                self.generic.append(v)
            
    def readPort(self):
        portRecReg = re.compile('\s*(\S+)\s*:\s*(\S+)\s*([^;]+)\s*;?', re.IGNORECASE)
        for line in forBracketBlock(self.lineGen):
            m= portRecReg.match(line)
            if m:
                v = BasicVariable(m.group(1), m.group(2),m.group(3))
                self.port.append(v)

    def __repr__(self):
        return "<VHDL.Entity %s>" % (self.name)