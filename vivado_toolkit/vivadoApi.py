from vivado_toolkit.vivadoController import VivadoTCL
import os

class Pin():
    def __init__(self, bd, name, hasSubIntf=False):
        self.bd = bd
        self.name = name
        self.hasSubIntf = hasSubIntf

    def get(self):
        if self.hasSubIntf:
            yield VivadoTCL.get_bd_intf_pins([self.name])
        else:
            yield VivadoTCL.get_bd_pins([self.name])

class Port():
    def __init__(self, bd, name, direction=None, typ=None, hasSubIntf=False):
        self.bd = bd
        self.name = name
        self.direction = direction
        self.typ = typ
        self.hasSubIntf = hasSubIntf
    
    def create(self):
        yield VivadoTCL.create_bd_port(self.name, self.direction, self.typ)    
            
    def get(self):
        if self.hasSubIntf:
            yield VivadoTCL.get_bd_intf_ports([self.name])
        else:
            yield VivadoTCL.get_bd_ports([self.name])

class Unit():
    def __init__(self, bd, ipCore, name):
        self.bd = bd
        self.ipCore = ipCore
        self.name = name
        self.pins = {}
        
    def create(self):
        yield VivadoTCL.create_bd_cell(self.ipCore, self.name)

    def get(self):
        yield VivadoTCL.get_bd_cells([self.name])

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
        src = ' '.join(self.src.get())
        dst = ' '.join(self.dst.get())
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

    def port(self, name):
        return Port(self, name)
    
    def importFromTcl(self, fileName, refrestIfExists=True):
        """
        @param refrestIfExists: refresh tcl file from bd before opening design
        """
        p = os.path
        assert(self.name == p.splitext(p.basename(fileName))[0])  # assert name of bd in tcl is correct
                    
        # update tcl from bd
        if p.exists(self.bdFile) and refrestIfExists:
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
        yield VivadoTCL.set_property("[current_fileset]", 'top', self.name + "_wrapper") 
        
    def unit(self, name, ipCore=None):
        return Unit(name, ipCore=ipCore)
    
    def regenerateLayout(self):
        yield VivadoTCL.regenerate_bd_layout()
    
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
        
    def get(self):
        return "[current_project]"    
    
    def updateAllCompileOrders(self):
        for g in self.listFileGroups():
            yield VivadoTCL.update_compile_order(g)
    
    def run(self, jobName):
        yield VivadoTCL.reset_run(jobName)
        yield VivadoTCL.launch_runs([jobName])
                
    def synthAll(self):
        for s in self.listSynthesis():
            yield from self.run(s)
            
    def implemAll(self):
        for s in self.listIpmplementations():
            yield from self.run(s)
    
    def listSynthesis(self):
        # [TODO] not ideal
        for p in filter(lambda d: d.startswith('synth'),
                        os.listdir(os.path.join(self.path, self.name + ".runs"))):
            yield p
            
    def listIpmplementations(self):
        # [TODO] not ideal
        for p in filter(lambda d: d.startswith('impl'),
                        os.listdir(os.path.join(self.path, self.name + ".runs"))):
            yield p
            
    def listFileGroups(self):
        for p in filter(os.path.isdir, os.listdir(self.srcDir)):
            yield os.path.basename(p)
                      
    def setPart(self, partName):
        yield VivadoTCL.set_property(self.get(), "part", partName)
        
    def setIpRepoPaths(self, paths):
        yield VivadoTCL.set_property(self.get(), valList=paths)
        yield VivadoTCL.update_ip_catalog()              
    
    def open(self):
        yield VivadoTCL.open_project(self.projFile)
        
    def close(self):
        yield VivadoTCL.close_project()   
         
    def boardDesign(self, name):
        return BoardDesign(self, name)
    
    
