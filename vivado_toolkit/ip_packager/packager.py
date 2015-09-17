import os, shutil
from os.path import basename, relpath
from vhdl_toolkit.parser import entityFromFile
from python_toolkit.fileHelpers import find_files
from vivado_toolkit.ip_packager.helpers import prettify
from vivado_toolkit.ip_packager.component import Component
from vivado_toolkit.ip_packager.blockRamWrap import blockRamWrap

def makeDummyXGUIFile(fileName):
    s = """
    # Definitional proc to organize widgets for parameters.
proc init_gui { IPINST } {
  #Adding Page
  ipgui::add_page $IPINST -name "Page 0"

}"""
    with open(fileName, "w") as f:
        f.write(s)

def packageMultipleProjects(workspace, names, ipRepo):
    for folder, name in names.items():
        packageVivadoHLSProj(os.path.join(workspace, folder), "solution1", name + ".vhd", ipRepo)
        print(folder + " packaged")

class Packager(object):
    def __init__(self, topEntity, vhdlDirs=[]):
        self.topEntity = topEntity
        self.vhdlFiles = []
        self.beforeBuilding = []
        for d in vhdlDirs:
            for f in find_files(d, "*.vhd"):
                self.vhdlFiles.append(f)
        

    def createPackage(self, repoDir):
        ip_dir = os.path.join(repoDir, self.topEntity.name + "/")      
        if os.path.exists(ip_dir):
            shutil.rmtree(ip_dir)
        
        ip_srcPath = os.path.join(ip_dir, "src")  
        tclPath = os.path.join(ip_dir, "xgui")  
        guiFile = os.path.join(tclPath, "gui.tcl")       
        for d in [ip_dir , ip_srcPath, tclPath]:
            os.makedirs(d)
        for f in self.vhdlFiles:
            shutil.copy2(f, ip_srcPath + "/")
        for p in self.beforeBuilding:
            p(self, ip_srcPath)
            
        makeDummyXGUIFile(guiFile)
        
        c = Component()
        c._files = list(
                        map(lambda p : os.path.join("src/" , p),
                            map(lambda p :basename(p), self.vhdlFiles)) \
                    ) \
                    + [relpath(guiFile, ip_dir) ]
        c.vendor = "nic"
        c.library = "mylib"
        c.description = self.topEntity.name + "_v" + c.version
        c.asignTopEntity(self.topEntity)
        xml_str = prettify(c.xml()) 
        with open(ip_dir + "component.xml", "w") as f:
            f.write(xml_str)

def packageVivadoHLSProj(projPath, solutionName, mainVhdlFileName, ipRepo):
    # rm others ip in project
    vhdlPath = os.path.join(projPath, solutionName, "syn/vhdl")   
    e = entityFromFile(os.path.join(vhdlPath, mainVhdlFileName))
    p = Packager(e, [vhdlPath])
    p.beforeBuilding.append(blockRamWrap)
    p.createPackage(ipRepo)

def packageBD(bdPath, repoPath):
    bdName = os.path.basename(bdPath)
    bdSourcesDir = os.path.join(bdPath, "hdl")
    vhldFolders = []
    ips_path = os.path.join(bdPath, "ip/")
    vhldFolders += [os.path.join(x[0], "synth") for x in os.walk(ips_path)]  # synth subfolder of each ip 
    vhldFolders += [bdSourcesDir]
    # ip folder 
    vhldFolders += [os.path.join(bdPath, "../../ipshared")]
    e = entityFromFile(os.path.join(bdSourcesDir, bdName + ".vhd"))
    p = Packager(e, vhldFolders)
    p.createPackage(ipRepo)
    
        

def demo():
    c_folder = "/home/nic30/Documents/vivado/ip_repo/component_test/"
    e = entityFromFile(c_folder + "src/component1.vhd")
    c = Component()
    c.vendor = "nic"
    c.library = "mylib"
    c.description = e.name + "_v" + c.version
    c._files = ["src/component1.vhd", "xgui/component1_v1_0.tcl" ]
    c.asignTopEntity(e)
    xml_str = prettify(c.xml()) 
    with open(c_folder + "component.xml", "w") as f:
        f.write(xml_str)
    print(xml_str)

if __name__ == "__main__":
    ipRepo = "/home/nic30/Documents/ip_repo"
    packageMultipleProjects("/home/nic30/Documents/vivado_hls/", {  # "axi_custom_master": "axi_custom_master",
                                                                 # "axi_trans_tester2": "axi_trans_tester",
                                                                 "superDMA": "superDMA",
                                                             #    "SuperDMA_inBuffer":"SuperDMA_inBuffer",
                                                                 # "axi_ch_a": "axi_native_intf",
                                                               #  "MultiFIFO_test":"MultiFifo_top"
                                                                 },
                                                                   ipRepo)
    #packageBD("/home/nic30/Documents/vivado/axi_trans_tester2/axi_trans_tester2.srcs/sources_1/bd/axi_tester_complex", ipRepo)
