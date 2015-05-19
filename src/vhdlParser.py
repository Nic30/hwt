import re, codecs
from models import Architecture, Entity, entityReg, architectureReg
from helpers import detectEncoding


class VhdlParser(object):
    def __init__(self, fileNames):
        self.fileNames = fileNames
        self.entities = []
        self.architectures = []
        self.ErrorList = []
    
    def load(self):
        for file in self.fileNames:
            sourceFile = self._withoutComments(file)
            try:
                for line in sourceFile:
                    mE = entityReg.match(line)
                    mA = architectureReg.match(line)
                    if mE :
                        e = Entity(mE.group(1), sourceFile, file)
                        self.entities.append(e)
                    if mA:
                        a = Architecture(mA.group(1), mA.group(2), sourceFile, file)
                        self.architectures.append(a)
                    
            except StopIteration:
                e = Exception("file %s is defect" % file)
                self.ErrorList.append(e)
                raise e
                #print(self.entities)
                #print(self.architectures)
        self.asignArchToEnt()
        
    def _withoutComments(self, file):
        en = detectEncoding(file)
        def splitOn(splitedLine, splitingReg):
            """splitingReg should be ("replacestr", re.compile("searchParent")) """
            for s in splitedLine:
                for item in splitingReg[1].sub("\n"+splitingReg[0]+"\n",s).split("\n"):
                    yield item
            
                   
        with codecs.open(file, encoding=en) as f:
            splits = [("(" ,re.compile("\(")),
                      (")",re.compile("\)")),
                      ("is", re.compile("(?<!\w)is(?!\w)", re.IGNORECASE)),
                      ("then", re.compile("(?<!\w)then(?!\w)", re.IGNORECASE)),
                      ("begin", re.compile("(?<!\w)begin(?!\w)", re.IGNORECASE)),
                      ("generate", re.compile("(?<!\w)generate(?!\w)", re.IGNORECASE)),
                      ("elsif", re.compile("(?<!\w)elsif(?!\w)", re.IGNORECASE))]
            generateFix = re.compile("end generate", re.IGNORECASE)
                
            for line in f:
                line = line.split("--")[0].lower().strip()
                if len(line) == 0:
                    continue
                line = [generateFix.sub("end", line)]
                for r in splits:
                    line = splitOn(line, r)
                
                for t in line:
                    s= t.strip()
                    if len(s) >0:
                        yield s 
 
    @classmethod
    def listMapedEntities(cls, o):
        if isinstance(o, Architecture):
            for pm in o.portMaps:
                yield pm.entityName
        else:
            if isinstance(o, Entity):
                for a in o.architectures:
                    for pm in VhdlParser.listMapedEntities(a):
                        yield pm
            else:
                e = Exception("Unknow object in listMapedEntities", o)
                raise e
            
    def asignArchToEnt(self):
        self.entDict = {}
        for e in self.entities:
            e.isRoot = True
            # if e.name in self.entDict.keys():
                # print("redefinition of entity %s, comes from file %s last was from %s" % (e.name, e.filename, self.entDict[e.name].filename))
            self.entDict[e.name] = e 

        # asign portmaps        
        for a in self.architectures:
            try:
                for pm in a.portMaps:
                    e = self.entDict[pm.entityName]
                    pm.entity = self.entDict[pm.entityName]
                    e.isRoot = False
                    a.entities.append(e)
            except KeyError as ke:
                print("missing entity %s for arch %s in file %s" % (pm.entityName, a.name, a.filename ))

        for a in self.architectures:
            try:
                self.entDict[a.entityName].architectures.append(a)
            except KeyError as ke:
                print( "missing entity %s" % (ke))

                
    @classmethod
    def entAsJson(cls, entity, rootId=None):
        childs = list(cls.listMapedEntities(entity))
        if rootId:
            childs = childs + [rootId]
        yield {
                "id": entity.name,
                "Edge": childs,
                "Type" :  "Entity",
                "FileName" : entity.filename
               }
        for a in entity.architectures:
            yield {
                   "id" : a.name,
                   "Type" : "Architecture",
                   "Edge" : [a.entityName],
                   "FileName" : a.filename
                   }
            for e in a.entities:
                for j in cls.entAsJson(e, entity.name):
                    yield j

    def vhdlsJsonReport(self):
        roots = filter(lambda e : e.isRoot , self.entities)
        
        for e in roots:
            for j in VhdlParser.entAsJson(e):
                yield j
