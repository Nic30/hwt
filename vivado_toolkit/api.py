from vivado_toolkit.controller import VivadoTCL
from vivado_toolkit.xdcGen import PackagePin, Comment
import os
import shutil

class ConfigErr(Exception):
    pass

class Pin():
    def __init__(self, bd, name, hasSubIntf=False):
        self.bd = bd
        self.name = name
        self.hasSubIntf = hasSubIntf

    def get(self):
        if self.hasSubIntf:
            return VivadoTCL.get_bd_intf_pins([self.name])
        else:
            return VivadoTCL.get_bd_pins([self.name])

class Port():
    def __init__(self, bd, name, direction=None, typ=None, hasSubIntf=False,
                 config=None, width=None, bitIndx=None):
        self.bd = bd
        self.name = name
        self.direction = direction
        self.typ = typ
        self.hasSubIntf = hasSubIntf
        if config is None:
            config = {} 
        self.config = config
        self.extraXDC = []
        self.bitIndx = bitIndx
        self.width = width
        if width is not None:
            assert(not bitIndx)
            assert(width > 0)
            self.bits = [Port(bd, name, direction=direction, typ=typ, bitIndx=i) for i in range(width)]
            
        else:
            self.bits = None
        if bitIndx is None:
            self.bd.insertPort(self)
            
    def create(self):
        yield VivadoTCL.create_bd_port(self.name, self.direction,
                                       typ=self.typ, width=self.width)    
        for k, v in self.config.items():
            yield VivadoTCL.set_property('[' + self.get() + ']', "CONFIG." + k, v)
    
    def forEachBit(self, fn):
        if self.bits:
            for bit in self.bits:
                fn(bit)
        else:
            fn(self)
    
    def generateXDC(self, portMap):
        if self.bits:
            yield Comment(self.name)
            for b in self.bits:
                yield from b.generateXDC(portMap)
        else:
            pin = portMap[self.name.lower()]
            if self.bitIndx is not None:
                if isinstance(pin, str):
                    raise ConfigErr("%s is vector and portMap contains only one bit" % (self.name))
                yield Comment(self.name + "[%d]" % self.bitIndx)
                try:
                    pin = pin[self.bitIndx]
                except IndexError:
                    raise ConfigErr("%s missing configuration for bit %d" % (self.name, self.bitIndx))
            else:
                yield Comment(self.name)
            assert(isinstance(pin, str))
            yield PackagePin(self, pin)
        
        for xdc in self.extraXDC:
            yield xdc
                
    def get(self, forHdlWrapper=False):
        name = self.name
        if self.bitIndx is not None:
            name = "{%s[%d]}" % (name, self.bitIndx)

        names = [name]

        if forHdlWrapper:
            if self.hasSubIntf:
                raise NotImplemented()
            else:
                return VivadoTCL.get_ports(names)
        else:
            if self.hasSubIntf:
                return VivadoTCL.get_bd_intf_ports(names)
            else:
                return VivadoTCL.get_bd_ports(names)

class Unit():
    def __init__(self, bd, ipCore, name):
        self.bd = bd
        self.ipCore = ipCore
        self.name = name
        self.pins = {}
        
    def create(self):
        yield VivadoTCL.create_bd_cell(self.ipCore, self.name)

    def get(self):
        return VivadoTCL.get_bd_cells([self.name])

    def pin(self, name, hasSubIntf=False):
        realPinName = "/%s/%s" % (self.name, name)
        p = self.pins.get(realPinName, None)
        if p:
            return p
        else:
            p = Pin(self.bd, realPinName, hasSubIntf=hasSubIntf)
            self.pins[realPinName] = p
            
            return p
    def set(self, config):
        yield VivadoTCL.set_property(VivadoTCL.get_bd_cells([self.name]), valDict=config)
        
class Net():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        
    def create(self):
        src = self.src.get()
        dst = self.dst.get()
        if self.src.hasSubIntf:
            yield VivadoTCL.connect_bd_intf_net(src, dst)
        else:
            yield VivadoTCL.connect_bd_net(src, dst)
        
    @classmethod
    def createMultipleFromDict(cls, netDict):
        for src, dst in netDict.items():
            if isinstance(dst, list) or isinstance(dst, tuple):  # if has multiple dst create net for all of them
                for d in dst:
                    yield from cls(src, d).create()
            else:
                yield from cls(src, dst).create()
             
class BoardDesign():
    def __init__(self, project, name=None):
        j = os.path.join
        self.project = project
        self.name = name
        self.bdDir = j(self.project.bdSrcDir, self.name)
        self.bdFile = j(self.bdDir, name + ".bd")
        self.bdWrapperFile = j(self.bdDir , 'hdl', self.name + "_wrapper.vhd")
        self.ports = {}
            
    def create(self):
        yield  VivadoTCL.create_bd_design(self.name)    
    
    def delete(self, fromDisk=True):
        yield VivadoTCL.remove_files([self.bdFile])
        yield VivadoTCL.remove_files([self.bdWrapperFile])

        if fromDisk:
            yield VivadoTCL.file.delete([self.bdDir])
            yield VivadoTCL.file.delete([self.bdWrapperFile])
       
    def exist(self):
        return os.path.exists(self.bdFile)
  
    def open(self):
        yield VivadoTCL.open_bd_design(self.bdFile)

    def insertPort(self, port):
        name_l = port.name.lower()
        if name_l in self.ports:
            raise ConfigErr("%s port redefinition" % name_l)
        else:
            self.ports[name_l] = port
    
    def importFromTcl(self, fileName, refrestTclIfExists=True):
        """
        @param refrestIfExists: refresh tcl file from bd before opening design
        """
        p = os.path
        assert(self.name == p.splitext(p.basename(fileName))[0])  # assert name of bd in tcl is correct
                    
        # update tcl from bd
        if p.exists(self.bdFile) and refrestTclIfExists:
            yield from self.open()
            yield from self.exportToTCL(fileName, force=True)
    
        # tcl file does not contains revisions of ips
        yield VivadoTCL.update_ip_catalog()
        
        # remove old bd
        yield from self.delete()
        
        # import new from tcl
        yield VivadoTCL.source(fileName)
        
        # generate wrapper and set is as top
        yield from self.mkWrapper()

     
    def exportToTCL(self, fileName, force=False):
        yield VivadoTCL.write_bd_tcl(fileName, force=force)
    
    def mkWrapper(self):
        yield VivadoTCL.make_wrapper(self.bdFile)
        yield VivadoTCL.add_files([self.bdWrapperFile])
        yield from self.project.updateAllCompileOrders()

    def setAsTop(self):
        yield from self.project.setTop(self.name + "_wrapper")
        
    def unit(self, name, ipCore=None):
        return Unit(name, ipCore=ipCore)
    
    def regenerateLayout(self):
        yield VivadoTCL.regenerate_bd_layout()

class Language():
    verilog = "verilog"
    vhdl = 'VHDL'
    
class Project():
    def __init__(self, path, name):
        """
        @param path: path is path of directory where project is stored
        @name name: name of project folder and project *.xpr/ppr file 
        """
        self.name = name
        self.path = os.path.join(path, name)
        self.projFile = os.path.join(path, name, name + ".xpr")
        self.srcDir = os.path.join(path, name, name + ".srcs/sources_1")  # [TODO] needs to be derived from fs or project
        self.bdSrcDir = os.path.join(self.srcDir, 'bd')
        self.constrFileSet_name = 'constrs_1'
        self.part = None
        self.top = None
    
    def create(self, in_memory=False):
        yield VivadoTCL.create_project(self.path, self.name, in_memory=in_memory)
        yield from self.setTargetLangue(Language.vhdl)
    
    def _exists(self):
        return os.path.exists(self.path)
    
    def _remove(self):
        shutil.rmtree(self.path)
        
    def get(self):
        return "[current_project]"    
    
    def updateAllCompileOrders(self):
        for g in self.listFileGroups():
            yield VivadoTCL.update_compile_order(g)
    
    def run(self, jobName, to_step=None):
        yield VivadoTCL.reset_run(jobName)
        yield VivadoTCL.launch_runs([jobName], to_step=to_step)
                
    def synthAll(self):
        for s in self.listSynthesis():
            yield from self.run(s)
            
    def synth(self):
        assert(self.top is not None)
        yield VivadoTCL.synth_design(self.top, self.part)
        
    def implemAll(self):
        for s in self.listIpmplementations():
            yield from self.run(s)
    
    def writeBitstream(self):
        yield from self.run("impl_1", to_step="write_bitstream")  # impl_1 -to_step write_bitstream -jobs 8
    
    def listSynthesis(self):
        # [TODO] not ideal
        for p in filter(lambda d: d.startswith('synth'),
                        os.listdir(os.path.join(self.path, self.name + ".runs"))):
            yield p
            
    def listIpmplementations(self):
        # [TODO] not ideal
        try:
            for p in filter(lambda d: d.startswith('impl'),
                            os.listdir(os.path.join(self.path, self.name + ".runs"))):
                yield p
        except FileNotFoundError:
            yield 'impl_1'  # project was not created yet
            
    def listFileGroups(self):
        try:
            for p in filter(os.path.isdir, os.listdir(self.srcDir)):
                yield os.path.basename(p)
        except FileNotFoundError:
            yield from ["sources_1", "constrs_1", "sim_1"]
    
    def setPart(self, partName):
        self.part = partName
        yield VivadoTCL.set_property(self.get(), "part", partName)
        
    def setIpRepoPaths(self, paths):
        yield VivadoTCL.set_property(self.get(), name='ip_repo_paths', valList=paths)
        yield VivadoTCL.update_ip_catalog()              
    
    def open(self):
        yield VivadoTCL.open_project(self.projFile)
        
    def close(self):
        yield VivadoTCL.close_project()   
         
    def boardDesign(self, name):
        return BoardDesign(self, name)
    
    def addDesignFiles(self, files):
        yield VivadoTCL.add_files(files)
        yield VivadoTCL.update_compile_order("sources_1")
    
    def setTop(self, topEntName):
        self.top = topEntName
        yield VivadoTCL.set_property("[current_fileset]", 'top', topEntName) 
    
    def addXDCs(self, name, XDCs):
        filename = os.path.join(self.srcDir, name + '.xdc') 
        with open(filename, "w") as f:
            f.write('\n'.join(map(lambda xdc : xdc.asTcl(), XDCs)))
        yield VivadoTCL.add_files([filename], fileSet=self.constrFileSet_name, norecurse=True)
    
    def setTargetLangue(self, lang):
        assert(lang == Language.verilog or lang == Language.vhdl)
        yield VivadoTCL.set_property(self.get(), "target_language", lang)
        
        
                    
