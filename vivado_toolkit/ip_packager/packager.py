import os, shutil
from os.path import basename, relpath

from python_toolkit.fileHelpers import find_files
from vhdl_toolkit.parser import entityFromFile
from vivado_toolkit.ip_packager.component import Component
from vivado_toolkit.ip_packager.helpers import prettify
from vhdl_toolkit.synthetisator.interfaceLevel.unit import defaultUnitName
from vhdl_toolkit.architecture import Architecture
from vhdl_toolkit.entity import Entity
from vhdl_toolkit.formater import formatVhdl



def makeDummyXGUIFile(fileName):
    s = """
    # Definitional proc to organize widgets for parameters.
proc init_gui { IPINST } {
  #Adding Page
  ipgui::add_page $IPINST -name "Page 0"

}"""
    with open(fileName, "w") as f:
        f.write(s)


class Packager(object):
    def __init__(self, topUnit, extraVhdlDirs=[], extraVhdlFiles=[]):
        self.topUnit = topUnit
        self.name =  defaultUnitName(self.topUnit)
        self.vhdlFilesToCopy = []
        self.beforeBuilding = []
        self.vhdlFiles = set()
        for d in extraVhdlDirs:
            for f in find_files(d, "*.vhd"):
                self.vhdlFilesToCopy.append(f)
        for f in extraVhdlFiles:
            self.vhdlFilesToCopy.append(f)
        
        
    def synthetizeAndSave(self, srcDir):
        path = os.path.join(srcDir, self.name)
        try: 
            os.makedirs(path)
        except OSError:
            # wipe if exists
            shutil.rmtree(path)
            os.makedirs(path)
        
        filesToCopy = set()
        filesToCopy.update(self.vhdlFilesToCopy)
        header = ''
        for o in self.topUnit._synthesise():
            if hasattr(o, '_origin'):
                filesToCopy.add(o._origin)
            else:
                toFile = None
                if isinstance(o, str): # [TODO] hotfix
                    header = o
                elif isinstance(o, Entity):
                    toFile = os.path.join(srcDir, o.name+'_ent.vhd')
                elif isinstance(o, Architecture):
                    toFile = os.path.join(srcDir, o.entity.name+'_arch.vhd')
                else:
                    raise NotImplementedError()
                if toFile:
                    with open(toFile, mode='w') as f:
                            s = formatVhdl(header + '\n'+ str(o))
                            f.write(s)
                            self.vhdlFiles.add(toFile)
        
        for srcF in filesToCopy:
            dst = os.path.join(path, os.path.relpath(srcF, srcDir).replace('../', ''))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(srcF, dst)
            self.vhdlFiles.add(dst)
    
    def createPackage(self, repoDir):
        
        ip_dir = os.path.join(repoDir, self.name + "/")      
        if os.path.exists(ip_dir):
            shutil.rmtree(ip_dir)
        
        ip_srcPath = os.path.join(ip_dir, "src")  
        tclPath = os.path.join(ip_dir, "xgui")  
        guiFile = os.path.join(tclPath, "gui.tcl")       
        for d in [ip_dir , ip_srcPath, tclPath]:
            os.makedirs(d)
        self.synthetizeAndSave(ip_srcPath)
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
        c.description = self.name + "_v" + c.version
        c.asignTopUnit(self.topUnit)
        xml_str = prettify(c.xml()) 
        with open(ip_dir + "component.xml", "w") as f:
            f.write(xml_str)

def packageMultipleProjects(workspace, names, ipRepo):
    for folder, name in names.items():
        packageVivadoHLSProj(os.path.join(workspace, folder), "solution1", name + ".vhd", ipRepo)
        print(folder + " packaged")

def packageVivadoHLSProj(projPath, solutionName, mainVhdlFileName, ipRepo):
    # rm others ip in project
    vhdlPath = os.path.join(projPath, solutionName, "syn/vhdl")   
    e = entityFromFile(os.path.join(vhdlPath, mainVhdlFileName))
    p = Packager(e, [vhdlPath])
    p.createPackage(ipRepo)

def packageBD(ipRepo, bdPath, repoPath):
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
      

if __name__ == "__main__":
    from vhdl_toolkit.samples.iLvl.bram import Bram
    from vhdl_toolkit.samples.iLvl.simple2 import  SimpleUnit2
    repo = '/home/nic30/Documents/test_ip_repo'
    u = Bram()
    u2 = SimpleUnit2()
    p = Packager(u)
    p.createPackage(repo)
    
    p = Packager(u2)
    p.createPackage(repo)
    
    
    #ipRepo = "/home/nic30/Documents/ip_repo"
    #packageMultipleProjects("/home/nic30/Documents/vivado_hls/", {  # "axi_custom_master": "axi_custom_master",
    #                                                             # "axi_trans_tester2": "axi_trans_tester",
    #                                                             "superDMA": "superDMA",
    #                                                         #    "SuperDMA_inBuffer":"SuperDMA_inBuffer",
    #                                                             # "axi_ch_a": "axi_native_intf",
    #                                                           #  "MultiFIFO_test":"MultiFifo_top"
    #                                                             },
    #                                                               ipRepo)
    ##packageBD("/home/nic30/Documents/vivado/axi_trans_tester2/axi_trans_tester2.srcs/sources_1/bd/axi_tester_complex", ipRepo)
