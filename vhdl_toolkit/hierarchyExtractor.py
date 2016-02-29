from vhdl_toolkit.parser import parseVhdl
from vhdl_toolkit.hdlObjects.reference import VhdlRef
import multiprocessing
from multiprocess.pool import Pool
from python_toolkit.arrayQuery import arr_any

class DesignFile():
    def __init__(self, fileName, hdlCtx):
        self.fileName = fileName
        self.hdlCtx = hdlCtx
        self.dependentOnFiles = set()
        
    @classmethod
    def fromFile(cls, f, libName='work', hdlCtx=None):
        return cls(f, parseVhdl([f], hdlCtx=hdlCtx, libName=libName, timeoutInterval=180, hierarchyOnly=True))
    
    def allDefinedRefs(self):
        for eName in self.hdlCtx.entities:
            yield VhdlRef([eName])
        for pName, p in self.hdlCtx.packages.items():
            if not p._isDummy:
                yield VhdlRef([pName])
        
    def allDependencies(self):
        # packageHeader < ent|arch|package
        # ent <- arch
        for _, e in self.hdlCtx.entities.items():
            yield from e.dependencies
            
        for a in self.hdlCtx.architectures:
            yield from a.dependencies
            yield VhdlRef([a.entityName])
            for ci in a.componentInstances:
                yield ci.entityRef
        
        for p in self.hdlCtx.packages:
            yield VhdlRef([p])
            
    @staticmethod
    def refMatch(iHad, iWontToHave):
        iwNames = iter(iWontToHave.names)
        ihNames = iter(iHad.names)
        if iWontToHave.names[0] == 'work':
            next(iwNames)
        for nh in ihNames: 
            try:
                nw = next(iwNames)
            except StopIteration:
                return True
            if nh != nw:
                return False
            try:
                nw = next(iwNames)
            except StopIteration:
                return True
            return False
        
    def findDependency(self, d, allDesignFiles):
        for df in allDesignFiles:
                for defDep in df.allDefinedRefs():
                    if DesignFile.refMatch(defDep, d):
                        return df.fileName
                           
    def discoverDependentOnFiles(self, allDesignFiles, ignoredRefs=[]):
        for d in self.allDependencies():
            if arr_any(ignoredRefs, lambda x: DesignFile.refMatch(d, x)):
                continue
            df = self.findDependency(d, allDesignFiles)
            if not df:
                raise Exception("%s: require to import %s and it is not defined in any file" % 
                                (self.fileName, str(d)))
            self.dependentOnFiles.add(df)
    
    @staticmethod
    def loadFiles(files, libName='work', parallel=True):
        if parallel:
            pool = Pool(multiprocessing.cpu_count())
            designFiles = pool.map(lambda f : DesignFile.fromFile(f, libName=libName), files)
        else:
            designFiles = []
            for f in  files:
                d = DesignFile(f, parseVhdl([f], hierarchyOnly=True))
                designFiles.append(d)
        return designFiles
    
    @staticmethod
    def fileDependencyDict(designFiles, ignoredRefs=[VhdlRef(["ieee"])]):
        depDict = {}
        for df in designFiles:
            df.discoverDependentOnFiles(designFiles, ignoredRefs)
            depDict[df.fileName] = df.dependentOnFiles            
        return depDict

def findFileWhereNameIsDefined(designFiles, name):
    targetRef = VhdlRef([name])
    for df in designFiles:
        refs = df.allDefinedRefs()
        for ref in refs:
            if DesignFile.refMatch(ref, targetRef):
                return df
