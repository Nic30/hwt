from vhdl_toolkit.parser import parseVhdl
from python_toolkit.fileHelpers import find_files
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
    def fromFile(cls, f):
        return cls(f, parseVhdl([f], timeoutInterval=180, hierarchyOnly=True))
    
    def allDefinedRefs(self):
        for eName in self.hdlCtx.entities:
            yield VhdlRef([eName])
        for ph in self.hdlCtx.packageHeaders:
            yield VhdlRef([ph])
        
    def allDependencies(self):
        # packageHeader < ent|arch|package
        # ent <- arch
        for _, e in self.hdlCtx.entities.items():
            yield from e.dependencies
            
        for a in self.hdlCtx.architectures:
            yield from a.dependencies
            yield VhdlRef([a.entityName])
        
        for p in self.hdlCtx.packages:
            yield VhdlRef([p])
    @staticmethod
    def refMatch(iHad, iWontToHave):
        iwNames = iter(iWontToHave.names)
        for nh in iHad.names:
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

               
if __name__ == "__main__":
    # ctx= parseVhdl(['/home/nic30/Downloads/fpgalibs/src/flt/sprobe1_filter/comp/config_adapter_arch.vhd'])
    projectDir = "/home/nic30/Downloads/fpgalibs/src/"
    # baseDir = projDir + "mem/dp_bram/"
    # fEnt = baseDir + "dp_bram_ent.vhd"
    # fArch = baseDir + "dp_bram_ent.vhd"
    # fPack = projDir + 'util/pkg/math_func.vhd'
    # print(fEnt)
    # e = process([fEnt])
    # projectDir = 'samples/iLvl/vhdl/dependencies0/'
    # projectDir = '/home/nic30/Documents/workspace/sprobe10/core/'
    files = list(find_files(projectDir, "*.vhd"))
    # designFiles = []
    # for f in  files:
    #    d = DesignFile(f, parseVhdl([f], hierarchyOnly=True))
    #    designFiles.append(d)
       
    pool = Pool(multiprocessing.cpu_count())
    designFiles = pool.map(DesignFile.fromFile, files)
    ignoredRefs = [VhdlRef(["ieee"])]
    def allDefined():
        for df in designFiles:
            for ref in df.allDefinedRefs(): 
                print(ref, '                ', df.fileName)
    allDefined()
    # for df in designFiles:
    #    df.discoverDependentOnFiles(designFiles, ignoredRefs)
    #    print(df.fileName)
    #    print(">>> " , df.dependentOnFiles, '\n')
    #    
    #    # print("defined", list(df.allDefinedRefs()))
    #    # print("required", list(df.allDependencies()))
    #
