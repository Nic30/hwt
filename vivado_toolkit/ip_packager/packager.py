import os, shutil
from os.path import basename, relpath

from python_toolkit.fileHelpers import find_files
from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.synthetisator.interfaceLevel.unit import defaultUnitName
from vhdl_toolkit.hdlObjects.architecture import Architecture
from vhdl_toolkit.hdlObjects.entity import Entity
from vhdl_toolkit.formater import formatVhdl
from vivado_toolkit.ip_packager.component import Component
from vivado_toolkit.ip_packager.helpers import prettify
from vivado_toolkit.ip_packager.tclGuiBuilder import GuiBuilder, paramManipulatorFns

class Packager(object):
    def __init__(self, topUnit, extraVhdlDirs=[], extraVhdlFiles=[],
                 extraVerilogFiles=[], extraVerilogDirs=[]):
        self.topUnit = topUnit
        self.name = defaultUnitName(self.topUnit)
        self.hdlFiles = set()
        
        for d in extraVhdlDirs:
            for f in find_files(d, "*.vhd"):
                self.hdlFiles.add(f)
        for f in extraVhdlFiles:
            self.hdlFiles.add(f)
        
        for d in extraVerilogDirs:
            for f in find_files(d, "*.v"):
                self.hdlFiles.add(f)
        for f in extraVerilogFiles:
            self.hdlFiles.add(f)
        
        
    def saveHdlFiles(self, srcDir):
        path = os.path.join(srcDir, self.name)
        try: 
            os.makedirs(path)
        except OSError:
            # wipe if exists
            shutil.rmtree(path)
            os.makedirs(path)
        
        files = self.hdlFiles
        header = ''
        for o in self.topUnit._synthesise():
            if hasattr(o, '_origin'):
                files.add(o._origin)
            else:
                toFile = None
                if isinstance(o, str):  # [TODO] hotfix, library includes are just strings
                    header = o
                elif isinstance(o, Entity):
                    toFile = os.path.join(srcDir, o.name + '_ent.vhd')
                elif isinstance(o, Architecture):
                    toFile = os.path.join(srcDir, o.entity.name + '_arch.vhd')
                else:
                    raise NotImplementedError()
                if toFile:
                    with open(toFile, mode='w') as f:
                            s = formatVhdl(header + '\n' + str(o))
                            f.write(s)
                            files.add(toFile)
        
        for srcF in files:
            dst = os.path.join(path, os.path.relpath(srcF, srcDir).replace('../', ''))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(srcF, dst)
            
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

    def createPackage(self, repoDir):
        '''
        synthetise hdl if needen
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
        c._files = [relpath(p, ip_dir) for p in self.hdlFiles] \
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
