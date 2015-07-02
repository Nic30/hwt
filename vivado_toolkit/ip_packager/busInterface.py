

from vivado_toolkit.ip_packager.helpers import appendSpiElem, \
         mkSpiElm, spi_ns_prefix
from vivado_toolkit.ip_packager.others import Parameter
from python_toolkit.arrayQuery import single, where

         
class IfConfig():
    dir_out, dir_in = ("out", "in")
    ifMaster, ifSlave = ("master", "slave")
    
    def findPort(self, logName):
        logName = logName.lower()
        p = single(self.port, lambda x : x.logName.lower() == logName)
        return p

    @classmethod
    def opositDir(cls, _dir_):
        if _dir_ == cls.dir_out:
            return cls.dir_in
        elif _dir_ == cls.dir_in:
            return cls.dir_out
        else:
            raise Exception()
    @classmethod
    def master(cls):
        self = cls()
        if len(self.port) == 0:
            raise Exception
        return self
    
    @classmethod
    def slave(cls):
        self = cls()
        sPort = []
        for p in self.port:
            sPort.append((p[0], cls.opositDir(p[1])))
        return self
    
    @classmethod
    def postProcess(cls, component, entity, allInterfaces, thisIfPrefix):
        pass 

class IfConfMap():
    def __init__(self, logName, phyName=None, masterDir=IfConfig.dir_in):
        self.logName = logName
        if phyName is None:
            self.phyName = "_" + logName.lower()
        else:
            self.phyName = phyName
        self.masterDir = masterDir
    def __repr__(self):
        return "<IfConfMap {%s:%s}>" % (self.logName, self.phyName)

class Handshake(IfConfig):
    def __init__(self):
        self.name = "handshake"
        self.version = "1.0"
        self.vendor = "nic" 
        self.library = "user"
        c = IfConfMap
        self.port = [c("ap_vld", masterDir=self.dir_out),
                     c("ap_ack", masterDir=self.dir_in),
                     c("data", masterDir=self.dir_out)
                     ]
        
class Handshake2(Handshake):
    def __init__(self):
        super().__init__()
        c = IfConfMap
        self.port = [c("ap_vld", masterDir=self.dir_out),
                     c("ap_ack", masterDir=self.dir_in),
                     c("data", "", masterDir=self.dir_out)
                     ]
        
class HS_config_d(Handshake):
    def __init__(self):
        super().__init__()
        c = IfConfMap
        self.port = [c("ap_vld", masterDir=self.dir_out),
                     c("ap_ack", masterDir=self.dir_in),
                     c("data", "_d", masterDir=self.dir_out)
                     ]

        
class Ap_clk(IfConfig):
    def __init__(self):
        self.name = "clock"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "signal"
        c = IfConfMap
        self.port = [c("CLK", "ap_clk", masterDir=self.dir_out)
                     ]
            
    # ASSOCIATED_BUSIF ASSOCIATED_RESET
    @classmethod                 
    def postProcess(cls, component, entity, allInterfaces, thisIf):
            rst = list(where(allInterfaces, lambda intf: intf._ifCls  in [Ap_rst, Ap_rst_n]))
            if len(rst) > 0:
                p = Parameter()
                p.name = "ASSOCIATED_RESET"
                p.value.resolve = "immediate"
                p.value.id = "BUSIFPARAM_VALUE." + thisIf.name + ".ASSOCIATED_RESET"
                p.value.text = rst[0]._portMaps['rst']  # getResetPortName
                thisIf.parameters.append(p)
            elif len(rst) > 1:
                raise Exception("Dont know how to work with multiple resets")
            
            intfs = where(allInterfaces, lambda intf: intf._ifCls not  in  [Ap_clk, Ap_rst, Ap_rst_n])
            p = Parameter()
            p.name = "ASSOCIATED_BUSIF"
            p.value.resolve = "immediate"
            p.value.id = "BUSIFPARAM_VALUE." + thisIf.name + ".ASSOCIATED_BUSIF"
            p.value.text = ":".join(map(lambda intf: intf.name, intfs))
            thisIf.parameters.append(p)
            p = Parameter()
            p.name = "FREQ_HZ"
            p.value.resolve = "immediate"
            p.value.id = "BUSIFPARAM_VALUE." + thisIf.name + ".FREQ_HZ"
            p.value.text = str(102000000)  # zynq std.
            thisIf.parameters.append(p)
            


class Ap_rst(IfConfig):
    def __init__(self):
        self.name = "reset"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "signal"
        c = IfConfMap
        self.port = [c("rst", "ap_rst", masterDir=self.dir_out)]
        
    @classmethod                 
    def postProcess(cls, component, entity, allInterfaces, thisIf):
        p = Parameter()
        p.name = "POLARITY"
        p.value.resolve = "immediate"
        p.value.id = "BUSIFPARAM_VALUE." + thisIf.name + ".POLARITY"
        p.value.text = "ACTIVE_HIGH"
        thisIf.parameters.append(p)

class Ap_rst_n(IfConfig):
    def __init__(self):
        self.name = "reset"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "signal"
        c = IfConfMap
        self.port = [c("rst", "ap_rst_n", masterDir=self.dir_out)]
        
    @classmethod                 
    def postProcess(cls, component, entity, allInterfaces, thisIf):
        p = Parameter()
        p.name = "POLARITY"
        p.value.resolve = "immediate"
        p.value.id = "BUSIFPARAM_VALUE.AP_RST_N.POLARITY"
        p.value.text = "ACTIVE_LOW"
        thisIf.parameters.append(p)


class AXILite(IfConfig):
    def __init__(self):
        self.name = "aximm"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "interface"
        c = IfConfMap
        self.port = [c("AWADDR", masterDir=self.dir_out),
                     c("AWVALID", masterDir=self.dir_out),
                     c("AWREADY", masterDir=self.dir_in),
                     
                     c("WDATA", masterDir=self.dir_out),
                     c("WSTRB", masterDir=self.dir_out),
                     c("WVALID", masterDir=self.dir_out),
                     c("WREADY", masterDir=self.dir_in),
                     
                     c("ARADDR", masterDir=self.dir_out),
                     c("ARVALID", masterDir=self.dir_out),
                     c("ARREADY", masterDir=self.dir_in),
                     
                     c("RDATA", masterDir=self.dir_in),
                     c("RRESP", masterDir=self.dir_in),
                     c("RVALID", masterDir=self.dir_in),
                     c("RREADY", masterDir=self.dir_out),

                     c("BVALID", masterDir=self.dir_in),
                     c("BREADY", masterDir=self.dir_out),
                     c("BRESP", masterDir=self.dir_in) 

                     ]

    @classmethod                 
    def postProcess(cls, component, entity, allInterfaces, thisIf):
        def getMyPortWidth(name):
            name = cls.master().findPort(name).phyName
            dim = single(component.model.ports, lambda p : p.name.lower() == (thisIf.name + name).lower()).vector
            return abs(dim[0] - dim[1]) + 1
        thisIf.endianness = "little"
        p_aw = Parameter()
        p_aw.name = "ADDR_WIDTH"
        p_aw.value.resolve = "immediate"
        p_aw.value.id = "BUSIFPARAM_VALUE." + thisIf.name + ".ADDR_WIDTH"
        p_aw.value.text = getMyPortWidth("AWADDR")
        thisIf.parameters.append(p_aw)
        
        p_dw = Parameter()
        p_dw.name = "DATA_WIDTH"
        p_dw.value.resolve = "immediate"
        p_dw.value.id = "BUSIFPARAM_VALUE." + thisIf.name + ".DATA_WIDTH"
        p_dw.value.text = getMyPortWidth("WDATA")
        thisIf.parameters.append(p_dw)
        
        p_prot = Parameter()
        p_prot.name = "PROTOCOL"
        p_prot.value.resolve = "immediate"
        p_prot.value.id = "BUSIFPARAM_VALUE." + thisIf.name + ".PROTOCOL"
        p_prot.value.text = "AXI4LITE"
        thisIf.parameters.append(p_prot)
        
        p_rw = Parameter()
        p_rw.name = "READ_WRITE_MODE"
        p_rw.value.resolve = "immediate"
        p_rw.value.id = "BUSIFPARAM_VALUE." + thisIf.name + ".READ_WRITE_MODE"
        p_rw.value.text = "READ_WRITE"
        thisIf.parameters.append(p_rw)
        

class Axi(AXILite):
    def __init__(self):
        super().__init__()
        c = IfConfMap
        self.port += [
                      c("ARBURST", masterDir=self.dir_out),
                      c("ARCACHE", masterDir=self.dir_out),
                      c("ARID", masterDir=self.dir_out),
                      c("ARLEN", masterDir=self.dir_out),
                      c("ARLOCK", masterDir=self.dir_out),
                      c("ARPROT", masterDir=self.dir_out),
                      c("ARSIZE", masterDir=self.dir_out),
                      c("ARQOS", masterDir=self.dir_out),
                      
                      c("BID", masterDir=self.dir_in),
                      
                      c("AWBURST", masterDir=self.dir_out),
                      c("AWCACHE", masterDir=self.dir_out),
                      c("AWID", masterDir=self.dir_out),
                      c("AWLEN", masterDir=self.dir_out),
                      c("AWLOCK", masterDir=self.dir_out),
                      c("AWPROT", masterDir=self.dir_out),
                      c("AWSIZE", masterDir=self.dir_out),
                      c("AWQOS", masterDir=self.dir_out),
                      
                      
                      c("RID", masterDir=self.dir_in),
                      c("RLAST", masterDir=self.dir_in),
                      
                      c("WID", masterDir=self.dir_out),
                      c("WLAST", masterDir=self.dir_out),
                      ]
    
    
class Axi_channeled(Axi):
    def __init__(self):
        super().__init__()
        def splitPortName(name):
            if name.startswith("A"):
                return (name[:2], name[2:])
            if name[0] in ["B", "W", "R"]:
                return (name[0], name[1:])
            else:
                raise Exception()
        for p in self.port:
            ch, n = splitPortName(p.logName)
            p.phyName = "_" + ch + "_" + n
            if  n not in ["VALID", "READY" , "LAST"]:
                p.phyName += "_V" 

        
defaultBusResolve = [ Ap_clk, Ap_rst_n, Ap_rst, Axi, Axi_channeled, AXILite, Handshake, Handshake2, HS_config_d]


class Type():
    __slots__ = ['name', 'version', 'vendor', 'library']
     
    @classmethod 
    def fromElem(cls, elm):
        self = cls()
        for s in ['name', 'version', 'vendor', 'library']:
            setattr(self, s, elm.attrib[spi_ns_prefix + s])
        return self
    
    def asElem(self, elmName):
        e = mkSpiElm(elmName)
        for s in ['name', 'version', 'vendor', 'library']:
            e.attrib[spi_ns_prefix + s] = getattr(self, s)
        return e    
    
class BusInterface():
    def __init__(self):
        self.name = None
        self.busType = Type()
        self.abstractionType = Type()
        self.isMaster = None
        # logical : physical
        self._portMaps = {}
        self.parameters = [] 
        self._ifCls = None
        self.endianness = None
    # @classmethod
    # def fromElem(cls, elm):
    #    self = cls()
    #    self.name = elm.find('spirit:name', ns).text
    #    self.busType = Type.fromElem(elm.find('spirit:busType', ns))
    #    self.abstractionType = Type.fromElem(elm.find('spirit:abstractionType', ns))
    #    if elm.find('spirit:master', ns) is not None:
    #        self.isMaster = True
    #    elif elm.find('spirit:slave', ns) is not None:
    #        self.isMaster = False
    #    else:
    #        raise Exception("buss missing master/slave specification")
    #    self._portMaps = []
    #    for m in elm.find('spirit:_portMaps', ns):
    #        pm = PortMap.fromElem(m)
    #        self._portMaps.append(pm)
    #    
    #    self.parameters = []
    #    for p in elm.find('spirit:parameters', ns):
    #        p_obj = Parameter.fromElem(p)
    #        self.parameters.append(p_obj)
    #        
    #    return self
    
    def asElem(self):
        def mkPortMap(logicalName, physicalName):
            pm = mkSpiElm("portMap")
            appendSpiElem(appendSpiElem(pm, "logicalPort"), "name").text = logicalName
            appendSpiElem(appendSpiElem(pm, "physicalPort"), "name").text = physicalName
            return pm
        e = mkSpiElm("busInterface")
        appendSpiElem(e, 'name').text = self.name
        e.append(self.busType.asElem('busType'))
        e.append(self.abstractionType.asElem('abstractionType'))
        if self.isMaster:
            appendSpiElem(e, "master")
        else:
            appendSpiElem(e, "slave")
       
        pm = appendSpiElem(e, "portMaps")

        for lName, pName in sorted(self._portMaps.items(), key=lambda pm: pm[0]):
            pm.append(mkPortMap(lName, pName))
        if self.endianness is not None:
            appendSpiElem(e, "endianness").text = self.endianness
        if len(self.parameters) > 0:
            pm = appendSpiElem(e, "parameters")
            for p in self.parameters:
                pm.append(p.asElem())
        return e
    

