import xml.etree.ElementTree as etree
from time import  time
from vivado_toolkit.ip_packager.helpers import appendSpiElem, appendStrElements, \
         mkSpiElm, ns, whereEndsWithExt
from vivado_toolkit.ip_packager.model import Model, Port
from vivado_toolkit.ip_packager.busInterface import \
    IfConfig, BusInterface, Type, defaultBusResolve, AXILite
from python_toolkit.arrayQuery import single
from vivado_toolkit.ip_packager.others import VendorExtensions, FileSet, File, \
    Parameter, Value

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
        v.order = "1"
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
        for p in self._topEntity.port:
            self.model.ports.append(Port._entPort2CompPort(e, p))


        def extractBusInterfaces(interface):
            """
            @return: yields busInterfce objects for interface in entity 
            """
            m = interface.master()
            firstIntfPort = m.port[0]
            def firstPortInstances():
                """
                @return: entity ports whitch probably matches with this interface
                """
                for x in e.port:
                    if x.name.lower().endswith(firstIntfPort.phyName.lower()):
                        yield x
            def getIfPrefix(entPort, interfaceConf):
                pName = entPort.name.lower()
                iName = firstIntfPort.phyName.lower()
                if pName == iName:
                    return interfaceConf.name
                else:
                    return  pName[:-len(iName)]
            def getMap(ifprefix, intfCls, ent):
                """
                @return:None if intf. cant be mapped othervicese returns (master/slave, {logical : physical})
                """
                allMatch = True
                noneMatch = True
                ifMap = {}
                for bi in m.port:
                    ep = single(ent.port, lambda p : p.name.lower() == ifprefix + bi.phyName)
                    if ep is None:
                        return
                    dirMatches = ep.direction.lower() == bi.masterDir
                    allMatch = allMatch and dirMatches
                    noneMatch = noneMatch  and not dirMatches     
                    ifMap[bi.logName] = ifprefix + bi.phyName
                    
                if allMatch:
                    ifT = IfConfig.ifMaster
                elif noneMatch:
                    ifT = IfConfig.ifSlave
                else:
                    return

                return (ifT, ifMap)
            
            def getBusTypeFromConf(IfConfigObj):
                t = Type()
                for s in t.__slots__:
                    setattr(t, s, getattr(IfConfigObj, s))
                return t
                
            for fpi in firstPortInstances():
                ifName = getIfPrefix(fpi, m)
                if fpi.name == firstIntfPort.phyName:
                    ifPrefix = ""
                else:
                    ifPrefix = ifName
                ifMap = getMap(ifPrefix, interface, e)
                if ifMap:
                    bi = BusInterface()
                
                    if ifPrefix == "":
                        bi.name = m.name
                    else:
                        bi.name = ifName
                    bi.busType = getBusTypeFromConf(m)
                    bi.abstractionType = getBusTypeFromConf(m)
                    bi.abstractionType.name += "_rtl"
                    bi.isMaster = ifMap[0] == IfConfig.ifMaster
                    bi._portMaps = ifMap[1]
                    bi._ifCls = interface
                    yield bi
       
        
        for c in defaultBusResolve:
            for bi in extractBusInterfaces(c):
                self.busInterfaces.append(bi)
        
        for bi in self.busInterfaces:
            bi._ifCls.postProcess(self, self._topEntity, self.busInterfaces, bi)
                
            


