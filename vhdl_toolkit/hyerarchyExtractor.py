from vhdl_toolkit.parser import process



class DesignFile():
    def __init__(self, fileName, hdlCtx):
        self.fileName = fileName
        self.hdlCtx = hdlCtx
        
    def allDependentFiles(self):
        yield None    

if __name__ == "__main__":
    projDir = "/home/nic30/Downloads/fpgalibs/src/"
    baseDir = projDir + "mem/dp_bram/"
    fEnt = baseDir + "dp_bram_ent.vhd"
    fArch = baseDir + "dp_bram_ent.vhd"
    fPack = projDir + 'util/pkg/math_func.vhd'
    print(fEnt)
    e = process([fEnt])
