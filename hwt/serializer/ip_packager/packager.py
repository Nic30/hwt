import os, shutil
from os.path import relpath

from hwt.pyUtils.fileHelpers import find_files
from hwt.serializer.ip_packager.component import Component
from hwt.serializer.ip_packager.helpers import prettify
from hwt.serializer.ip_packager.tclGuiBuilder import GuiBuilder, paramManipulatorFns
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.synthesizer.shortcuts import toRtlAndSave
from hwt.synthesizer.uniqList import UniqList


# [TODO] memory maps https://forums.xilinx.com/t5/Embedded-Processor-System-Design/exporting-AXI-BASEADDR-to-xparameters-h-from-Vivado-IP/td-p/428650
class Packager(object):
    """
    Ipcore packager
    """
    def __init__(self, topUnit, name=None, extraVhdlDirs=[], extraVhdlFiles=[],
                 extraVerilogFiles=[], extraVerilogDirs=[],
                 serializer=VhdlSerializer):
        self.topUnit = topUnit
        self.serializer = serializer
        if name:
            self.name = name
        else:
            self.name = self.topUnit._getDefaultName()
        
        self.hdlFiles = UniqList()
        
        for d in extraVhdlDirs:
            for f in find_files(d, "*.vhd"):
                self.hdlFiles.append(f)
                
        for f in extraVhdlFiles:
            self.hdlFiles.append(f)
        
        for d in extraVerilogDirs:
            for f in find_files(d, "*.v"):
                self.hdlFiles.append(f)
                
        for f in extraVerilogFiles:
            self.hdlFiles.append(f)

    def saveHdlFiles(self, srcDir):
        path = os.path.join(srcDir, self.name)
        try: 
            os.makedirs(path)
        except OSError:
            # wipe if exists
            shutil.rmtree(path)
            os.makedirs(path)
        
        files = self.hdlFiles
        self.hdlFiles = UniqList(
                          toRtlAndSave(self.topUnit, folderName=path,
                          name=self.name, serializer=self.serializer)
                        )

        for srcF in files:
            dst = os.path.join(path, os.path.relpath(srcF, srcDir)\
                               .replace('../', ''))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(srcF, dst)
            self.hdlFiles.append(dst)
            
    def mkAutoGui(self):
        gui = GuiBuilder()
        p0 = gui.page("Page_0")
        handlers = []
        for g in  self.topUnit._entity.generics:
            p0.param(g.name)
            for fn in paramManipulatorFns(g.name):
                handlers.append(fn)
        with open(self.guiFile, "w") as f:
            s = gui.asTcl() + '\n' + '\n'.join(map(lambda x : str(x), handlers))
            f.write(s)

    def createPackage(self, repoDir, vendor="hwt", library="mylib", description=None):
        '''
        synthetise hdl if needed
        copy hdl files
        create gui file
        
        '''
        ip_dir = os.path.join(repoDir, self.name + "/")      
        if os.path.exists(ip_dir):
            shutil.rmtree(ip_dir)
        
        ip_srcPath = os.path.join(ip_dir, "src")  
        tclPath = os.path.join(ip_dir, "xgui")  
        guiFile = os.path.join(tclPath, "gui.tcl")       
        for d in [ip_dir , ip_srcPath, tclPath]:
            os.makedirs(d)
        self.saveHdlFiles(ip_srcPath)
        
        self.guiFile = guiFile    
        self.mkAutoGui()
        
        c = Component()
        c._files = [relpath(p, ip_dir) for p in sorted(self.hdlFiles)] \
                    + [relpath(guiFile, ip_dir) ]
        
        c.vendor = vendor
        c.library = library
        if description is None:
            c.description = self.name + "_v" + c.version
        else:
            c.description = description
            
        c.asignTopUnit(self.topUnit)
        
        xml_str = prettify(c.xml()) 
        with open(ip_dir + "component.xml", "w") as f:
            f.write(xml_str)

# def packageMultipleProjects(workspace, names, ipRepo):
#    for folder, name in names.items():
#        packageVivadoHLSProj(os.path.join(workspace, folder), "solution1", name + ".vhd", ipRepo)
#        print(folder + " packaged")
#
# def packageVivadoHLSProj(projPath, solutionName, mainVhdlFileName, ipRepo):
#    # rm others ip in project
#    vhdlPath = os.path.join(projPath, solutionName, "syn/vhdl")   
#    e = entityFromFile(os.path.join(vhdlPath, mainVhdlFileName))
#    p = Packager(e, [vhdlPath])
#    p.createPackage(ipRepo)
#
# def packageBD(ipRepo, bdPath, repoPath):
#    bdName = os.path.basename(bdPath)
#    bdSourcesDir = os.path.join(bdPath, "hdl")
#    vhldFolders = []
#    ips_path = os.path.join(bdPath, "ip/")
#    vhldFolders += [os.path.join(x[0], "synth") for x in os.walk(ips_path)]  # synth subfolder of each ip 
#    vhldFolders += [bdSourcesDir]
#    # ip folder 
#    vhldFolders += [os.path.join(bdPath, "../../ipshared")]
#    e = entityFromFile(os.path.join(bdSourcesDir, bdName + ".vhd"))
#    p = Packager(e, vhldFolders)
#    p.createPackage(ipRepo)
