from time import  time

from vivado_toolkit.ip_packager.busInterface import defaultBusResolve, extractBusInterface
from vivado_toolkit.ip_packager.helpers import appendSpiElem, appendStrElements, \
         mkSpiElm, ns, whereEndsWithExt
from vivado_toolkit.ip_packager.model import Model, Port
from vivado_toolkit.ip_packager.others import VendorExtensions, FileSet, File, \
    Parameter, Value
import xml.etree.ElementTree as etree


vhdl_syn_fileSetName = "xilinx_vhdlsynthesis_view_fileset"
vhdl_sim_fileSetName = "xilinx_vhdlbehavioralsimulation_view_fileset"
tcl_fileSetName = "xilinx_xpgui_view_fileset"

   
class Component():
    """
    Xilinx xml is element position dependent
    """
    _strValues = ["vendor", "library", "name", "version", "description"]
    # _iterableValues = ["fileSets", "parameters" ]
    def __init__(self): 
        self.vendor = ''
        self.library = ''
        self.name = ""
        self.version = "1.0"
        self.busInterfaces = []
        self.model = Model(vhdl_syn_fileSetName, vhdl_sim_fileSetName, tcl_fileSetName)
        self.fileSets = []
        self.description = ""
        self.parameters = []
        self.vendorExtensions = VendorExtensions()
        self._files = []
        self._topEntity = None
                      
    # @classmethod
    # def load(cls, xmlStr):
    #    self = cls()
    #    for prefix, uri in ns.items():
    #        etree.register_namespace(prefix, uri)
    #    self.root = etree.fromstring(xmlStr)
    #    self.name = findS(self.root, "name").text
    #    
    #    intf = findS(self.root, "busInterfaces")
    #    self.interfaces = {}
    #    for i in intf:
    #        i = BusInterface.fromElem(i)
    #        if i.name in self.interfaces.keys():
    #            raise Exception("Multiple interfaces with same name")
    #        self.interfaces[i.name] = i
    #    self.model = Model.fromElem(findS(self.root, "model"))
    #    
    #    return self
    
    def _xmlFileSets(self, componentElem):
        def fileSetFromFiles(name, files):
            fileSet = FileSet()
            fileSet.name = name
            for fn in files:
                f = File.fromFileName(fn)
                fileSet.files.append(f)
            return fileSet
        filesets = appendSpiElem(componentElem, "fileSets")
        vhdl_fs = fileSetFromFiles(vhdl_syn_fileSetName, whereEndsWithExt(self._files, ".vhd"))
        vhdl_sim_fs = fileSetFromFiles(vhdl_sim_fileSetName, whereEndsWithExt(self._files, ".vhd"))
        tclFileSet = fileSetFromFiles(tcl_fileSetName, whereEndsWithExt(self._files, ".tcl"))
        for fs in [vhdl_fs, vhdl_sim_fs, tclFileSet]:
            filesets.append(fs.asElem())
            

        
    def _xmlParameters(self, compElem):
        parameters = appendSpiElem(compElem, "parameters")
        compNameParam = Parameter()
        compNameParam.name = "Component_Name"
        compNameParam.value = Value()
        v = compNameParam.value
        v.id = "PARAM_VALUE.Component_Name"
        v.resolve = "user"
        v.text = self.name
        parameters.append(compNameParam.asElem())
        
    def xml(self):
        for prefix, uri in ns.items():
            etree.register_namespace(prefix, uri)
        c = mkSpiElm("component")
        appendStrElements(c, self, self._strValues[:-1])
        if len(self.busInterfaces) > 0:
            bi = appendSpiElem(c, "busInterfaces")
            for b in self.busInterfaces:
                bi.append(b.asElem())
        c.append(self.model.asElem())
        self._xmlFileSets(c)
        
        appendStrElements(c, self, [self._strValues[-1]])
        self._xmlParameters(c)
        c.append(self.vendorExtensions.asElem(self.name + "_v" + self.version, revision=str(int(time()))))
        
        return c
   
    
    def asignTopEntity(self, e):
        self._topEntity = e
        self.name = e.name
        self.model.addDefaultViews(self.name)
        def trimUnderscores(s):
            while s.endswith("_"):
                s = s[:-1]
            return s
        def removeUndescores_witSep(s, separator):
            if isinstance(s, str):
                return separator.join([ trimUnderscores(a) for a  in s.split(separator)])
            else:
                return s
        for p in self._topEntity.port:
            self.model.ports.append(Port._entPort2CompPort(e, p))

        for c in defaultBusResolve:
            for bi in extractBusInterface(self._topEntity, c):
                self.busInterfaces.append(bi)
                
       
        for bi in self.busInterfaces:
            bi._ifObj.postProcess(self, self._topEntity, self.busInterfaces, bi)
                
        for bi in self.busInterfaces:
            bi.name = trimUnderscores(bi.name)
            for p in bi.parameters:
                
                p.name = removeUndescores_witSep(p.name, ".")
                p.value.id = removeUndescores_witSep(p.value.id , ".")
                p.value.text = removeUndescores_witSep(p.value.text , ".")

            


